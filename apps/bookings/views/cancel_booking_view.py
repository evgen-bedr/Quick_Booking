# apps/booking/views/cancel_booking_view.py

from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.bookings.models.booking_model import Booking
from apps.bookings.serializers.booking_serializer import BookingSerializer
from apps.bookings.choises.booking_choice import BookingChoices


class CancelBookingView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def update(self, request, pk=None):
        try:
            booking = Booking.objects.get(pk=pk, user=request.user)
        except Booking.DoesNotExist:
            return Response({'error': 'Booking not found.'}, status=status.HTTP_404_NOT_FOUND)

        if booking.can_cancel():
            booking.status = BookingChoices.CANCELLED
            booking.save()
            serializer = BookingSerializer(booking)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'error': 'Cannot cancel booking past the cancellation deadline.'},
                        status=status.HTTP_400_BAD_REQUEST)
