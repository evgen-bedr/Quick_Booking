# apps/search_and_filters/views/search_view.py
from django.db.models import Q, Case, When, IntegerField, Value, Sum
from django.db.models.functions import Coalesce
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

from apps.rentals.models.rental_model import Rental
from apps.rentals.serializers.rental_serializer import RentalSerializer
from apps.search_and_filters.models.search_model import SearchHistory, UserSearchHistory
from apps.search_and_filters.serializers.search_serializer import SearchHistorySerializer

class SearchViewSet(viewsets.ModelViewSet):
    serializer_class = RentalSerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Rental.objects.with_average_rating().filter(status=True, verified=True).order_by('-created_at')
        query = self.request.GET.get('q', '').strip()
        user = self.request.user

        # Сохраняем поисковый запрос только если он не пустой и пользователь аутентифицирован
        if query and user.is_authenticated:
            search_history, created = SearchHistory.objects.get_or_create(search_query=query)
            if created:
                search_history.search_count = 1
            else:
                search_history.search_count += 1
            search_history.save()
            UserSearchHistory.objects.create(user=user, search_history=search_history)

        filters = {
            'min_price': self.request.GET.get('min_price'),
            'max_price': self.request.GET.get('max_price'),
            'location': self.request.GET.getlist('location'),
            'city': self.request.GET.getlist('city'),
            'country': self.request.GET.get('country'),
            'rooms': self.request.GET.get('rooms'),
            'property_type': self.request.GET.getlist('property_type'),
            'tags': self.request.GET.getlist('tags'),
            'min_views': self.request.GET.get('min_views'),
            'max_views': self.request.GET.get('max_views'),
            'min_rating': self.request.GET.get('min_rating'),
            'max_rating': self.request.GET.get('max_rating'),
            'min_reviews': self.request.GET.get('min_reviews'),
            'max_reviews': self.request.GET.get('max_reviews')
        }
        sort_by = self.request.GET.get('sort_by', 'created_at')
        sort_order = self.request.GET.get('sort_order', 'asc')

        sort_fields = {
            'created_at': 'created_at',
            'min_price': 'price',
            'max_price': '-price',
            'min_rating': 'average_rating',
            'max_rating': '-average_rating',
            'min_reviews': 'reviews_count',
            'max_reviews': '-reviews_count',
            'min_views': 'views_count',
            'max_views': '-views_count'
        }

        sort_by_field = sort_fields.get(sort_by, 'created_at')
        if sort_order == 'desc':
            sort_by_field = '-' + sort_by_field.lstrip('-')

        results = queryset

        # Поиск по ключевым словам в тайтле и описании
        q_objects = Q()
        if query:
            exact_match_results = results.filter(
                Q(title__icontains=query) | Q(description__icontains=query)
            )
            if exact_match_results.exists():
                results = exact_match_results
            else:
                query_words = query.split()
                for word in query_words:
                    q_objects |= Q(title__icontains=word) | Q(description__icontains=word)
                results = results.filter(q_objects)

        # Применение фильтров
        if filters['min_price']:
            results = results.filter(price__gte=filters['min_price'])
        if filters['max_price']:
            results = results.filter(price__lte=filters['max_price'])
        if filters['location']:
            for location in filters['location']:
                results = results.filter(location__icontains=location)
        if filters['city']:
            for city in filters['city']:
                results = results.filter(city__icontains=city)
        if filters['country']:
            results = results.filter(country__icontains=filters['country'])
        if filters['rooms']:
            results = results.filter(rooms=filters['rooms'])
        if filters['property_type']:
            for property_type in filters['property_type']:
                results = results.filter(property_type__iexact=property_type)
        if filters['tags']:
            for tag in filters['tags']:
                results = results.filter(tags__name__icontains=tag)
        if filters['min_views']:
            results = results.filter(views_count__gte=filters['min_views'])
        if filters['max_views']:
            results = results.filter(views_count__lte=filters['max_views'])
        if filters['min_rating']:
            results = results.filter(average_rating__gte=filters['min_rating'])
        if filters['max_rating']:
            results = results.filter(average_rating__lte=filters['max_rating'])
        if filters['min_reviews']:
            results = results.filter(reviews_count__gte=filters['min_reviews'])
        if filters['max_reviews']:
            results = results.filter(reviews_count__lte=filters['max_reviews'])

        # Ранжирование результатов
        when_conditions = []
        if query:
            when_conditions.append(When(Q(title__icontains=query) | Q(description__icontains=query), then=1))
            if not q_objects == Q():
                when_conditions.append(When(q_objects, then=2))

        results = results.annotate(
            rank=Case(
                *when_conditions,
                default=3,
                output_field=IntegerField()
            )
        ).order_by('rank', sort_by_field)

        return results

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def popular_searches(self, request):
        popular_searches = SearchHistory.objects.values('search_query').annotate(
            total=Sum('search_count')).order_by('-total')[:10]
        return Response(popular_searches, status=status.HTTP_200_OK)
