from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.search_and_filters.models.search_model import UserSearchHistory
from apps.search_and_filters.serializers.search_serializer import UserSearchHistorySerializer


class UserSearchHistoryViewSet(viewsets.ViewSet):
    """
    Handles operations for managing a user's search history.

    @permission_classes: [IsAuthenticated] : List : Permissions required to access the view
    """
    permission_classes = [IsAuthenticated]

    def list(self, request):
        """
        List all search history records for the authenticated user, with optional sorting.

        @param request: Request : The request object containing query parameters

        @return: Response : JSON response with the list of search history records or error message
        """
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
        """
        Retrieve the search history records for a specific user by user ID, with optional sorting.

        @param request: Request : The request object containing query parameters
        @param pk: str : The primary key representing the user ID

        @return: Response : JSON response with the user's search history records or error message
        """
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
            return Response({'detail': 'No search history found for the given user ID.'},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = UserSearchHistorySerializer(search_history, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
