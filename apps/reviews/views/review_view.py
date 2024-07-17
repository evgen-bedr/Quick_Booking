from rest_framework import viewsets, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied, ValidationError
from apps.reviews.models.review_model import Review
from apps.reviews.serializers.review_serializer import ReviewSerializer
from apps.bookings.models.create_booking_model import Booking
from apps.rentals.models.rental_model import Rental
from apps.core.permissions.moderator_or_super import IsModeratorOrSuperUser
from apps.core.utils.rating_utils import update_rating_and_reviews  # измените импорт


class ReviewViewSet(viewsets.ModelViewSet):
    """
        ReviewViewSet is a viewset for handling operations on reviews. It allows
        authenticated users to create, update, delete, and list reviews for a specific
        rental property.

        Permissions:
            - Only authenticated users can perform actions on reviews.
            - Only the user who created the review can update it.
            - Only a moderator or superuser can delete reviews.

        Methods:
            - get_queryset: Returns the queryset of reviews for the specified rental.
            - perform_create: Handles creating a new review, ensuring the user has a
              confirmed or completed booking for the rental, and that the review is unique.
            - perform_update: Handles updating an existing review, ensuring the user has
              permission and a valid booking for the rental.
            - destroy: Handles deleting a review, ensuring the user has the appropriate
              permissions.

        Русская документация:
        ReviewViewSet - это viewset для обработки операций с отзывами. Он позволяет
        аутентифицированным пользователям создавать, обновлять, удалять и просматривать
        отзывы для конкретного объекта аренды. Используется пагинация для ограничения
        количества отзывов на страницу.

        Разрешения:
            - Только аутентифицированные пользователи могут выполнять действия с отзывами.
            - Только пользователь, создавший отзыв, может его обновить.
            - Только модератор или суперпользователь могут удалять отзывы.

        Методы:
            - get_queryset: Возвращает набор отзывов для указанного объекта аренды.
            - perform_create: Обрабатывает создание нового отзыва, обеспечивая наличие у
              пользователя подтвержденного или завершенного бронирования для аренды и
              уникальность отзыва.
            - perform_update: Обрабатывает обновление существующего отзыва, обеспечивая
              наличие у пользователя прав и действующего бронирования для аренды.
            - destroy: Обрабатывает удаление отзыва, обеспечивая наличие у пользователя
              соответствующих прав.
        """
    permission_classes = [IsAuthenticated]
    serializer_class = ReviewSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        return Review.objects.filter(rental__id=self.kwargs['rental_id'])

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

        if booking.status not in ['Confirmed', 'Completed']:
            raise ValidationError('Only confirmed or completed bookings can be reviewed.')

        if Review.objects.filter(user=user, rental=rental).exists():
            raise ValidationError('You have already reviewed this rental.')

        if rating is None and not comment:
            raise ValidationError('At least one of rating or comment must be provided.')

        serializer.save(user=user, rental=rental, booking=booking)
        update_rating_and_reviews(rental)  # вызов утилиты

    def perform_update(self, serializer):
        review = self.get_object()
        if review.user != self.request.user:
            raise PermissionDenied("You do not have permission to edit this review.")

        if not Booking.objects.filter(user=self.request.user, rental=review.rental,
                                      status__in=['Confirmed', 'Completed']).exists():
            raise PermissionDenied("You do not have a confirmed or completed booking for this rental.")

        serializer.save()
        update_rating_and_reviews(review.rental)  # вызов утилиты

    def destroy(self, request, *args, **kwargs):
        review = self.get_object()
        if not IsModeratorOrSuperUser().has_permission(request, self):
            raise PermissionDenied("You do not have permission to delete this review.")
        rental = review.rental
        self.perform_destroy(review)
        update_rating_and_reviews(rental)  # вызов утилиты
        return Response(status=status.HTTP_204_NO_CONTENT)

    # def partial_update(self, request, *args, **kwargs):
    #     review = self.get_object()
    #     if review.user != self.request.user:
    #         raise PermissionDenied("You do not have permission to edit this review.")
    #
    #     if not Booking.objects.filter(user=self.request.user, rental=review.rental, status='Confirmed').exists():
    #         raise PermissionDenied("You do not have a confirmed booking for this rental.")
    #
    #     return super().partial_update(request, *args, **kwargs)
