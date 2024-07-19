from rest_framework import viewsets, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied, ValidationError

from apps.bookings.choises.booking_choice import BookingChoices
from apps.reviews.models.review_model import Review
from apps.reviews.serializers.review_serializer import ReviewSerializer
from apps.bookings.models.booking_model import Booking
from apps.rentals.models.rental_model import Rental
from apps.core.utils.rating_utils import update_rating_and_reviews


class ReviewViewSet(viewsets.ModelViewSet):
    """
    Handles CRUD operations for reviews.

    @permission_classes: [IsAuthenticatedOrReadOnly] : List : Permissions required to access the view
    @serializer_class: ReviewSerializer : Serializer : Review serializer
    @pagination_class: PageNumberPagination : Pagination : Pagination class used by the viewset
    """
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = ReviewSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        """
        Retrieve the queryset of reviews for a specific rental, with optional sorting.

        @param self: ReviewViewSet : Instance of the viewset

        @return: QuerySet : Reviews for the specified rental, optionally sorted
        """
        if getattr(self, 'swagger_fake_view', False):
            return Review.objects.none()

        queryset = Review.objects.filter(rental__id=self.kwargs['rental_id']).order_by('-created_at')
        sort_by = self.request.query_params.get('sort_by', 'created_at')
        order_by = self.request.query_params.get('order_by', 'desc')

        valid_sort_fields = ['created_at', 'rating']
        if sort_by not in valid_sort_fields:
            sort_by = 'created_at'
        if order_by == 'desc':
            sort_by = f'-{sort_by}'
        return queryset.order_by(sort_by)

    def perform_create(self, serializer):
        """
        Handle the creation of a new review, with validation of rental and booking.

        @param serializer: Serializer : Serializer object containing validated data for the new review

        @raises: ValidationError : If rental or booking ID is invalid, booking is not completed, or user is not allowed to review

        @return: None
        """
        user = self.request.user
        rental_id = self.kwargs['rental_id']
        booking_id = self.request.data.get('booking')
        rating = self.request.data.get('rating')
        comment = self.request.data.get('comment')

        try:
            rental = Rental.objects.get(id=rental_id)
            booking = Booking.objects.get(id=booking_id)
        except (Rental.DoesNotExist, Booking.DoesNotExist):
            raise ValidationError('Invalid rental or booking ID.')

        if booking.user != user or booking.rental != rental:
            raise ValidationError('Invalid booking or you are not allowed to review this rental.')

        if booking.status != BookingChoices.COMPLETED:
            raise ValidationError('Only completed bookings can be reviewed.')

        if Review.objects.filter(user=user, rental=rental).exists():
            raise ValidationError('You have already reviewed this rental.')

        if rating is None and not comment:
            raise ValidationError('At least one of rating or comment must be provided.')

        serializer.save(user=user, rental=rental, booking=booking)
        update_rating_and_reviews(rental)

    def perform_update(self, serializer):
        """
        Update an existing review, with validation of user permissions and update of rental rating.

        @param serializer: Serializer : Serializer object containing validated data for the review update

        @raises: PermissionDenied : If the user does not have permission to edit the review

        @return: None
        """
        instance = self.get_object()
        user = self.request.user

        if user != instance.user and not (user.is_superuser or (hasattr(user, 'role') and user.role == 'Moderator')):
            raise PermissionDenied("You do not have permission to edit this review.")

        original_status = instance.status

        update_fields = serializer.validated_data.keys()
        changing_sensitive_fields = 'comment' in update_fields

        review = serializer.save()

        if changing_sensitive_fields:
            review.status = False
        else:
            review.status = original_status

        review.save()
        update_rating_and_reviews(review.rental)

    def destroy(self, request, *args, **kwargs):
        """
        Delete a review if the user has the necessary permissions, and update the rental's rating.

        @param request: Request : Request object containing the request data
        @param args: tuple : Additional positional arguments
        @param kwargs: dict : Additional keyword arguments

        @raises: PermissionDenied : If the user does not have permission to delete the review

        @return: Response : JSON response confirming the deletion
        """
        review = self.get_object()
        if not (request.user.is_superuser or (hasattr(request.user, 'role') and request.user.role == 'Moderator')):
            raise PermissionDenied("You do not have permission to delete this review.")
        rental = review.rental
        self.perform_destroy(review)
        update_rating_and_reviews(rental)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a specific review.

        @param request: Request : Request object containing the request data
        @param args: tuple : Additional positional arguments
        @param kwargs: dict : Additional keyword arguments

        @return: Response : JSON response with review details
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
