from django.db import models
from django.conf import settings
from datetime import datetime, timedelta
from apps.bookings.choises.booking_choice import BookingChoices
from apps.rentals.models.rental_model import Rental


class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rental = models.ForeignKey(Rental, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=BookingChoices.choices, default=BookingChoices.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    msg_to_landlord = models.TextField(null=True, blank=True)
    msg_to_user = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.rental.title} ({self.start_date} to {self.end_date})"

    def can_cancel(self):
        cancel_deadline = self.start_date - timedelta(days=7)
        return datetime.now().date() <= cancel_deadline

    def check_status(self):
        if self.end_date < datetime.now().date() and self.status == BookingChoices.CONFIRMED:
            self.status = BookingChoices.COMPLETED
            self.save()
