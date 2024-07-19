from django.db.models import Sum
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.search_and_filters.models.search_model import SearchHistory
from apps.search_and_filters.serializers.search_serializer import SearchHistorySerializer


class SearchHistoryViewSet(viewsets.ModelViewSet):
    queryset = SearchHistory.objects.all()
    serializer_class = SearchHistorySerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def popular_searches(self, request):
        popular_searches = SearchHistory.objects.values('search_query').annotate(
            total=Sum('search_count')).order_by('-total')[:10]
        return Response(popular_searches, status=status.HTTP_200_OK)
