# apps/booking/views/user_booking_list_view.py

from rest_framework import viewsets
from rest_framework.status import HTTP_200_OK
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.bookings.models.create_booking_model import Booking
from apps.bookings.serializers.booking_serializer import BookingSerializer


class UserBookingListView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        user = request.user
        sort_by = request.query_params.get('sort_by', 'created_at')
        order = request.query_params.get('order', 'desc')
        status_filters = request.query_params.getlist('status')

        valid_sort_fields = ['status', 'start_date', 'end_date', 'created_at']
        valid_statuses = ['Pending', 'Confirmed', 'Cancelled', 'Completed']

        if sort_by not in valid_sort_fields:
            sort_by = 'created_at'
        if order == 'desc':
            sort_by = f'-{sort_by}'

        bookings = Booking.objects.filter(user=user)

        if status_filters:
            status_filters = [status for status in status_filters if status in valid_statuses]
            if status_filters:
                bookings = bookings.filter(status__in=status_filters)

        bookings = bookings.order_by(sort_by)
        for booking in bookings:
            booking.check_status()
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data, status=HTTP_200_OK)
