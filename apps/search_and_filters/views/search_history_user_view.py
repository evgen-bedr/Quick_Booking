# apps/search_and_filters/views/search_history_user_view.py
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.search_and_filters.models.search_model import UserSearchHistory
from apps.search_and_filters.serializers.search_serializer import UserSearchHistorySerializer

class UserSearchHistoryViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        user = request.user
        sort_by = request.GET.get('sort_by', 'created_at')
        sort_order = request.GET.get('sort_order', 'desc')

        if sort_by not in ['created_at']:
            return Response({'detail': 'Invalid sort_by parameter.'}, status=status.HTTP_400_BAD_REQUEST)
        if sort_order not in ['asc', 'desc']:
            return Response({'detail': 'Invalid sort_order parameter.'}, status=status.HTTP_400_BAD_REQUEST)

        ordering = f"{'' if sort_order == 'asc' else '-'}{sort_by}"
        search_history = UserSearchHistory.objects.filter(user=user).order_by(ordering)
        serializer = UserSearchHistorySerializer(search_history, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        user = request.user

        try:
            user_id = int(pk)
        except ValueError:
            return Response({'detail': 'Invalid user ID.'}, status=status.HTTP_400_BAD_REQUEST)

        if user.id != user_id:
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)

        sort_by = request.GET.get('sort_by', 'created_at')
        sort_order = request.GET.get('sort_order', 'desc')

        if sort_by not in ['created_at']:
            return Response({'detail': 'Invalid sort_by parameter.'}, status=status.HTTP_400_BAD_REQUEST)
        if sort_order not in ['asc', 'desc']:
            return Response({'detail': 'Invalid sort_order parameter.'}, status=status.HTTP_400_BAD_REQUEST)

        ordering = f"{'' if sort_order == 'asc' else '-'}{sort_by}"
        search_history = UserSearchHistory.objects.filter(user_id=user_id).order_by(ordering)

        if not search_history.exists():
            return Response({'detail': 'No search history found for the given user ID.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserSearchHistorySerializer(search_history, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
