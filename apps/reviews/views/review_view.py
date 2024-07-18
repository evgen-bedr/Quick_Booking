# apps/reviews/views/review_view.py

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
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = ReviewSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
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
        review = self.get_object()
        if not (request.user.is_superuser or (hasattr(request.user, 'role') and request.user.role == 'Moderator')):
            raise PermissionDenied("You do not have permission to delete this review.")
        rental = review.rental
        self.perform_destroy(review)
        update_rating_and_reviews(rental)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
