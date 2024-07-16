# apps/booking/views/create_booking_view.py

from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.bookings.models.create_booking_model import Booking
from apps.bookings.serializers.booking_serializer import BookingSerializer
from apps.bookings.choises.booking_choice import BookingChoices
from apps.rentals.models.rental_model import Rental


class CreateBookingView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request):
        user = request.user
        rental_id = request.data.get('rental')
        start_date = request.data.get('start_date')
        end_date = request.data.get('end_date')
        msg_to_landlord = request.data.get('msg_to_landlord')

        rental = Rental.objects.get(id=rental_id)

        # Check if the rental is available for the given dates
        conflicting_bookings = Booking.objects.filter(rental=rental, status=BookingChoices.CONFIRMED).filter(
            start_date__lt=end_date, end_date__gt=start_date)
        if conflicting_bookings.exists():
            return Response({'error': 'The rental is not available for the selected dates.'},
                            status=status.HTTP_400_BAD_REQUEST)

        # Create the booking
        booking = Booking.objects.create(
            user=user,
            rental=rental,
            price=rental.price,  # Assuming rental has a price field
            start_date=start_date,
            end_date=end_date,
            status=BookingChoices.PENDING,
            msg_to_landlord=msg_to_landlord
        )
        serializer = BookingSerializer(booking)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
