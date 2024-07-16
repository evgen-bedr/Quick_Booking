# apps/core/management/commands/update_booking_statuses.py

from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.bookings.models.create_booking_model import Booking
from apps.bookings.choises.booking_choice import BookingChoices


class Command(BaseCommand):
    help = 'Update booking statuses to Completed if end_date is past'

    def handle(self, *args, **kwargs):
        now = timezone.now().date()
        bookings = Booking.objects.filter(status=BookingChoices.CONFIRMED, end_date__lt=now)
        for booking in bookings:
            booking.status = BookingChoices.COMPLETED
            booking.save(update_fields=['status'])
        self.stdout.write(self.style.SUCCESS('Updated booking statuses to Completed where end_date is past'))
