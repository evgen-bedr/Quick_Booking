from django.db.models import Q, Case, When, IntegerField, Value
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from apps.rentals.models.rental_model import Rental
from apps.rentals.serializers.rental_serializer import RentalSerializer
from apps.search_and_filters.models.search_model import SearchHistory

class SearchViewSet(viewsets.ViewSet):
    def list(self, request):
        query = request.GET.get('q', '').strip()
        user = request.user

        # Сохраняем поисковый запрос только если он не пустой
        if user.is_authenticated and query:
            search_history, created = SearchHistory.objects.get_or_create(user=user, search_query=query)
            if not created:
                search_history.search_count += 1
                search_history.save()

        filters = {
            'min_price': request.GET.get('min_price'),
            'max_price': request.GET.get('max_price'),
            'location': request.GET.getlist('location'),
            'city': request.GET.getlist('city'),
            'country': request.GET.get('country'),
            'rooms': request.GET.get('rooms'),
            'property_type': request.GET.getlist('property_type'),
            'tags': request.GET.getlist('tags'),
            'min_views': request.GET.get('min_views'),
            'max_views': request.GET.get('max_views'),
            'min_rating': request.GET.get('min_rating'),
            'max_rating': request.GET.get('max_rating'),
            'min_reviews': request.GET.get('min_reviews'),
            'max_reviews': request.GET.get('max_reviews')
        }
        sort_by = request.GET.get('sort_by', 'created_at')
        sort_order = request.GET.get('sort_order', 'asc')

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

        results = Rental.objects.all()

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

        # Пагинации
        paginator = PageNumberPagination()
        paginated_results = paginator.paginate_queryset(results, request)

        serializer = RentalSerializer(paginated_results, many=True)
        return paginator.get_paginated_response(serializer.data)
