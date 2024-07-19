from django.db.models import Sum
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.search_and_filters.models.search_model import SearchHistory
from apps.search_and_filters.serializers.search_serializer import SearchHistorySerializer


class SearchHistoryViewSet(viewsets.ModelViewSet):
    """
    Handles CRUD operations for search history.

    @queryset: SearchHistory.objects.all() : QuerySet : All search history records
    @serializer_class: SearchHistorySerializer : Serializer : Search history serializer
    @permission_classes: [IsAuthenticated] : List : Permissions required to access the view
    @lookup_field: 'id' : str : Field used for lookup by viewset
    """
    queryset = SearchHistory.objects.all()
    serializer_class = SearchHistorySerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def popular_searches(self, request):
        """
        Retrieve the top 10 popular search queries based on search count.

        @param request: Request : The request object containing the request data

        @return: Response : JSON response with the list of popular search queries and their counts
        """
        popular_searches = SearchHistory.objects.values('search_query').annotate(
            total=Sum('search_count')).order_by('-total')[:10]
        return Response(popular_searches, status=status.HTTP_200_OK)
