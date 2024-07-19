from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from apps.reviews.models.review_model import Review
from apps.reviews.serializers.review_serializer import ReviewSerializer


class UserReviewsViewSet(viewsets.ModelViewSet):
    """
    Handles operations for managing a user's reviews.

    @serializer_class: ReviewSerializer : Serializer : Review serializer
    @permission_classes: [IsAuthenticated] : List : Permissions required to access the view
    @pagination_class: PageNumberPagination : Pagination : Pagination class used by the viewset
    """
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        """
        Retrieve the queryset of reviews for the authenticated user, with optional sorting.

        @param self: UserReviewsViewSet : Instance of the viewset

        @return: QuerySet : Reviews for the authenticated user, optionally sorted
        """
        user = self.request.user
        queryset = Review.objects.filter(user=user).order_by('-created_at')

        sort_by = self.request.query_params.get('sort_by', 'created_at')
        order = self.request.query_params.get('order', 'desc')

        valid_sort_fields = ['created_at', 'rating']
        if sort_by not in valid_sort_fields:
            sort_by = 'created_at'
        if order == 'desc':
            sort_by = f'-{sort_by}'

        return queryset.order_by(sort_by)
