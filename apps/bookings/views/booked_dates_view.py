from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.bookings.models.booking_model import Booking
from datetime import timedelta


class BookedDatesViewSet(viewsets.ViewSet):
    """
    Handles retrieving booked dates for a specific rental.

    @permission_classes: [IsAuthenticated] : List : Permissions required to access the view
    """
    permission_classes = [IsAuthenticated]

    def list(self, request, rental_id=None):
        """
        Retrieve the list of booked dates for a specific rental.

        @param request: Request : Request object containing the request data
        @param rental_id: str : ID of the rental property

        @return: Response : JSON response with the list of booked dates or error message
        """
        if not rental_id:
            return Response({'error': 'Rental ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        confirmed_bookings = Booking.objects.filter(rental_id=rental_id, status='Confirmed').values('start_date',
                                                                                                    'end_date')
        booked_dates = []

        for booking in confirmed_bookings:
            start_date = booking['start_date']
            end_date = booking['end_date']
            current_date = start_date
            while current_date <= end_date:
                booked_dates.append(current_date)
                current_date += timedelta(days=1)

        return Response({'booked_dates': booked_dates}, status=status.HTTP_200_OK)
