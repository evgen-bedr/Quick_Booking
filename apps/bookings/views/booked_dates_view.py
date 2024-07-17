from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.bookings.models.create_booking_model import Booking
from datetime import datetime, timedelta


class BookedDatesViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request, rental_id=None):
        if not rental_id:
            return Response({'error': 'Rental ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        confirmed_bookings = Booking.objects.filter(rental_id=rental_id, status='Confirmed').values('start_date',
                                                                                                    'end_date')
        occupied_dates = []

        for booking in confirmed_bookings:
            start_date = booking['start_date']
            end_date = booking['end_date']
            current_date = start_date
            while current_date <= end_date:
                occupied_dates.append(current_date)
                current_date += timedelta(days=1)

        return Response({'occupied_dates': occupied_dates}, status=status.HTTP_200_OK)
