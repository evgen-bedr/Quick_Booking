# apps/bookings/views/booking_view.py

from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.bookings.models.booking_model import Booking
from apps.bookings.serializers.booking_serializer import BookingSerializer
from apps.bookings.choises.booking_choice import BookingChoices
from apps.rentals.models.rental_model import Rental
from datetime import datetime, timedelta


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
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

        # Check if start_date and end_date are not in the past
        if start_date_dt < datetime.now().date() or end_date_dt < datetime.now().date():
            return Response({'error': 'Start date and end date must be in the future.'},
                            status=status.HTTP_400_BAD_REQUEST)

        # Check if start_date is before end_date
        if start_date_dt > end_date_dt:
            return Response({'error': 'End date must be after start date.'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the rental is available for the given dates
        conflicting_bookings = Booking.objects.filter(
            rental=rental,
            status=BookingChoices.CONFIRMED
        ).filter(
            start_date__lt=end_date, end_date__gt=start_date
        )
        if conflicting_bookings.exists():
            return Response({'error': 'The rental is not available for the selected dates.'},
                            status=status.HTTP_400_BAD_REQUEST)

        # Calculate the number of days and total price
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
        user = self.request.user
        booking = self.get_object()

        if user != booking.user:
            return Response({'error': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)

        current_status = booking.status
        action = request.data.get('action')
        msg_to_landlord = request.data.get('msg_to_landlord')
        start_date = request.data.get('start_date')
        end_date = request.data.get('end_date')

        if msg_to_landlord:
            booking.msg_to_landlord = msg_to_landlord

        if start_date:
            start_date_dt = datetime.strptime(start_date, "%Y-%m-%d").date()
            if start_date_dt < datetime.now().date():
                return Response({'error': 'Start date must be in the future.'}, status=status.HTTP_400_BAD_REQUEST)
            booking.start_date = start_date_dt
        else:
            start_date_dt = booking.start_date

        if end_date:
            end_date_dt = datetime.strptime(end_date, "%Y-%m-%d").date()
            if end_date_dt < datetime.now().date():
                return Response({'error': 'End date must be in the future.'}, status=status.HTTP_400_BAD_REQUEST)
            if start_date_dt and start_date_dt > end_date_dt:
                return Response({'error': 'End date must be after start date.'}, status=status.HTTP_400_BAD_REQUEST)
            booking.end_date = end_date_dt
        else:
            end_date_dt = booking.end_date

        if current_status == BookingChoices.PENDING:
            if action == 'cancel':
                booking.status = BookingChoices.CANCELLED

        elif current_status == BookingChoices.CONFIRMED:
            days_until_start = (booking.start_date - datetime.now().date()).days
            if action == 'cancel' and days_until_start >= 3:
                booking.status = BookingChoices.CANCELLED
            else:
                return Response({'error': 'Cannot cancel booking within 3 days of start date.'},
                                status=status.HTTP_400_BAD_REQUEST)

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

        booking.save()
        serializer = self.get_serializer(booking)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
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
        user = request.user
        instance = self.get_object()
        if instance.user != user:
            return Response({'error': 'You do not have permission to access this booking.'},
                            status=status.HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        return response
