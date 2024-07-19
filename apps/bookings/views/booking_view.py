from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.bookings.models.booking_model import Booking
from apps.bookings.serializers.booking_serializer import BookingSerializer
from apps.bookings.choises.booking_choice import BookingChoices
from apps.rentals.models.rental_model import Rental
from datetime import datetime


class BookingViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling booking operations.

    @queryset: Booking.objects.all() : QuerySet : All bookings
    @serializer_class: BookingSerializer : Serializer : Booking serializer
    @permission_classes: [IsAuthenticated] : List : Permissions required to access the view
    """
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """
        Create a new booking.

        @param request: Request : The request object containing booking details
        @param args: tuple : Additional positional arguments
        @param kwargs: dict : Additional keyword arguments

        @return: Response : JSON response with booking details or error message
        """

        user = self.request.user
        rental_id = request.data.get('rental')
        start_date = request.data.get('start_date')
        end_date = request.data.get('end_date')
        msg_to_landlord = request.data.get('msg_to_landlord')

        try:
            rental = Rental.objects.get(id=rental_id)
        except Rental.DoesNotExist:
            return Response({'error': 'The rental does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        start_date_dt = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date_dt = datetime.strptime(end_date, "%Y-%m-%d").date()

        if start_date_dt < datetime.now().date() or end_date_dt < datetime.now().date():
            return Response({'error': 'Start date and end date must be in the future.'},
                            status=status.HTTP_400_BAD_REQUEST)

        if start_date_dt > end_date_dt:
            return Response({'error': 'End date must be after start date.'}, status=status.HTTP_400_BAD_REQUEST)

        conflicting_bookings = Booking.objects.filter(
            rental=rental,
            status=BookingChoices.CONFIRMED
        ).filter(
            start_date__lt=end_date, end_date__gt=start_date
        )
        if conflicting_bookings.exists():
            return Response({'error': 'The rental is not available for the selected dates.'},
                            status=status.HTTP_400_BAD_REQUEST)

        days = (end_date_dt - start_date_dt).days
        total_price = rental.price * days

        booking = Booking.objects.create(
            user=user,
            rental=rental,
            price=total_price,
            start_date=start_date_dt,
            end_date=end_date_dt,
            status=BookingChoices.PENDING,
            msg_to_landlord=msg_to_landlord
        )

        serializer = BookingSerializer(booking)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        """
        Update an existing booking.

        @param request: Request : The request object containing updated booking details
        @param args: tuple : Additional positional arguments
        @param kwargs: dict : Additional keyword arguments

        @return: Response : JSON response with updated booking details or error message
        """
        user = self.request.user
        booking = self.get_object()

        if user != booking.user:
            return Response({'error': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)

        current_status = booking.status
        action = request.data.get('action')
        msg_to_landlord = request.data.get('msg_to_landlord')
        start_date = request.data.get('start_date')
        end_date = request.data.get('end_date')

        days_until_start = (booking.start_date - datetime.now().date()).days

        if days_until_start <= 3:
            # If there are 3 days or less until the start date, only allow updating msg_to_landlord
            if msg_to_landlord:
                booking.msg_to_landlord = msg_to_landlord
            else:
                return Response({'error': 'Cannot update booking details within 3 days of start date.'},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            # Allow updating other fields if there are more than 3 days until the start date
            if msg_to_landlord:
                booking.msg_to_landlord = msg_to_landlord

            if start_date:
                start_date_dt = datetime.strptime(start_date, "%Y-%m-%d").date()
                if start_date_dt < datetime.now().date():
                    return Response({'error': 'Start date must be in the future.'}, status=status.HTTP_400_BAD_REQUEST)
                booking.start_date = start_date_dt
                booking.status = BookingChoices.PENDING

            if end_date:
                end_date_dt = datetime.strptime(end_date, "%Y-%m-%d").date()
                if end_date_dt < datetime.now().date():
                    return Response({'error': 'End date must be in the future.'}, status=status.HTTP_400_BAD_REQUEST)
                if start_date_dt and start_date_dt > end_date_dt:
                    return Response({'error': 'End date must be after start date.'}, status=status.HTTP_400_BAD_REQUEST)
                booking.end_date = end_date_dt
                booking.status = BookingChoices.PENDING

            if start_date or end_date:
                rental = booking.rental
                conflicting_bookings = Booking.objects.filter(
                    rental=rental,
                    status=BookingChoices.CONFIRMED
                ).filter(
                    start_date__lt=booking.end_date, end_date__gt=booking.start_date
                )
                if conflicting_bookings.exists():
                    return Response({'error': 'The rental is not available for the selected dates.'},
                                    status=status.HTTP_400_BAD_REQUEST)
                booking.price = (booking.end_date - booking.start_date).days * rental.price

        if current_status == BookingChoices.PENDING:
            if action == 'cancel':
                booking.status = BookingChoices.CANCELLED

        elif current_status == BookingChoices.CONFIRMED:
            if action == 'cancel' and days_until_start > 3:
                booking.status = BookingChoices.CANCELLED
            elif action == 'cancel':
                return Response({'error': 'Cannot cancel booking within 3 days of start date.'},
                                status=status.HTTP_400_BAD_REQUEST)

        booking.save()
        serializer = self.get_serializer(booking)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        """
        List all bookings for the authenticated user.

        @param request: Request : The request object containing query parameters
        @param args: tuple : Additional positional arguments
        @param kwargs: dict : Additional keyword arguments

        @return: Response : JSON response with list of bookings or error message
        """
        user = request.user
        queryset = self.get_queryset().filter(user=user).order_by("-created_at")

        # Sorting
        sort_by = request.query_params.get('sort_by', 'created_at')
        order = request.query_params.get('order', 'desc')
        valid_sort_fields = ['status', 'start_date', 'end_date', 'created_at', 'rental__title']

        if sort_by not in valid_sort_fields:
            sort_by = 'created_at'
        if order == 'desc':
            sort_by = f'-{sort_by}'

        queryset = queryset.order_by(sort_by)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a specific booking for the authenticated user.

        @param request: Request : The request object containing the booking ID
        @param args: tuple : Additional positional arguments
        @param kwargs: dict : Additional keyword arguments

        @return: Response : JSON response with booking details or error message
        """
        user = request.user
        instance = self.get_object()
        if instance.user != user:
            return Response({'error': 'You do not have permission to access this booking.'},
                            status=status.HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """
        Delete a specific booking.

        @param request: Request : The request object containing the booking ID
        @param args: tuple : Additional positional arguments
        @param kwargs: dict : Additional keyword arguments

        @return: Response : JSON response confirming deletion or error message
        """
        response = super().destroy(request, *args, **kwargs)
        return response
