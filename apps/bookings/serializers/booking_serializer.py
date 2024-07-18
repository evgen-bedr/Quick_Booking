# apps/bookings/serializers/booking_serializer.py
from rest_framework import serializers
from apps.bookings.models.booking_model import Booking

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'user', 'rental', 'price', 'start_date', 'end_date', 'status', 'created_at', 'updated_at', 'msg_to_landlord', 'msg_to_user']
        read_only_fields = ['user', 'price', 'status', 'created_at', 'updated_at']
