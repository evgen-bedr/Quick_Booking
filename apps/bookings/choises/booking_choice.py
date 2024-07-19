from django.db import models


class BookingChoices(models.TextChoices):
    PENDING = 'Pending', 'Pending'
    CONFIRMED = 'Confirmed', 'Confirmed'
    CANCELLED = 'Cancelled', 'Cancelled'
    COMPLETED = 'Completed', 'Completed'
