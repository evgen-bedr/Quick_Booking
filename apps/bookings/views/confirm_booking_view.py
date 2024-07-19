from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.bookings.models.booking_model import Booking
from apps.bookings.serializers.booking_serializer import BookingSerializer
from apps.bookings.choises.booking_choice import BookingChoices


class ConfirmBookingView(viewsets.ViewSet):
    """
    Handles booking confirmation or cancellation by the rental owner.

    @permission_classes: [IsAuthenticated] : List : Permissions required to access the view
    """
    permission_classes = [IsAuthenticated]

    def update(self, request, pk=None):
        """
        Confirm or decline a booking request by the rental owner.

        @param request: Request : Request object containing the request data
        @param pk: str : Primary key of the booking to be updated

        @return: Response : JSON response with updated booking details or error message
        """
        try:
            booking = Booking.objects.get(pk=pk)
        except Booking.DoesNotExist:
            return Response({'error': 'Booking not found.'}, status=status.HTTP_404_NOT_FOUND)

        if request.user == booking.rental.user:
            action = request.data.get('action')
            msg_to_user = request.data.get('msg_to_user')
            booking.msg_to_user = msg_to_user
            if action == 'confirm':
                booking.status = BookingChoices.CONFIRMED
            elif action == 'decline':
                booking.status = BookingChoices.CANCELLED
            booking.save()
            serializer = BookingSerializer(booking)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'error': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)
