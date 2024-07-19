from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from apps.bookings.models.booking_model import Booking
from apps.bookings.serializers.booking_serializer import BookingSerializer
from apps.bookings.choises.booking_choice import BookingChoices


class LandlordConfirmBookingViewSet(viewsets.ModelViewSet):
    """
    Handles booking confirmation or cancellation by landlords.

    @serializer_class: BookingSerializer : Serializer : Booking serializer
    @permission_classes: [IsAuthenticated] : List : Permissions required to access the view
    @pagination_class: PageNumberPagination : Pagination : Pagination class used by the viewset
    """
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        """
        Retrieve the queryset of bookings for the landlord, with optional sorting and filtering by status.

        @param self: LandlordConfirmBookingViewSet : Instance of the viewset

        @return: QuerySet : Filtered bookings based on user's role and status filters
        """
        user = self.request.user
        if user.role != 'Landlord':
            return Booking.objects.none()

        queryset = Booking.objects.filter(rental__user=user)
        status_filters = self.request.query_params.getlist('status')
        if status_filters:
            queryset = queryset.filter(status__in=status_filters)

        sort_by = self.request.query_params.get('sort_by', 'created_at')
        order = self.request.query_params.get('order', 'desc')
        valid_sort_fields = ['status', 'start_date', 'end_date', 'created_at', 'rental__title']

        if sort_by not in valid_sort_fields:
            sort_by = 'created_at'
        if order == 'desc':
            sort_by = f'-{sort_by}'

        return queryset.order_by(sort_by)

    def list(self, request, *args, **kwargs):
        """
        Retrieve a paginated list of bookings for the landlord.

        @param request: Request : Request object containing the request data
        @param args: tuple : Additional positional arguments
        @param kwargs: dict : Additional keyword arguments

        @return: Response : JSON response with paginated list of bookings
        """
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        """
        Confirm or decline a booking request by the landlord.

        @param request: Request : Request object containing the request data
        @param args: tuple : Additional positional arguments
        @param kwargs: dict : Additional keyword arguments

        @return: Response : JSON response with updated booking details or error message
        """
        user = self.request.user
        booking = self.get_object()

        if user != booking.rental.user:
            return Response({'error': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)

        action = request.data.get('action')
        msg_to_user = request.data.get('msg_to_user')
        if msg_to_user:
            booking.msg_to_user = msg_to_user

        if action == 'confirm':

            conflicting_bookings = Booking.objects.filter(
                rental=booking.rental,
                status=BookingChoices.CONFIRMED
            ).exclude(id=booking.id).filter(
                start_date__lt=booking.end_date, end_date__gt=booking.start_date
            )
            if conflicting_bookings.exists():
                return Response({'The rental is not longer available for the selected dates.'},
                                status=status.HTTP_400_BAD_REQUEST)

            booking.status = BookingChoices.CONFIRMED
        elif action == 'decline':
            booking.status = BookingChoices.CANCELLED

        booking.save()
        serializer = self.get_serializer(booking)
        return Response(serializer.data)
