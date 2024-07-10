from django.db import models


class Role(models.TextChoices):
    USER = 'User', 'User'
    LANDLORD = 'Landlord', 'Landlord'
    MODERATOR = 'Moderator', 'Moderator'
    BOOKING_MANAGER = 'Booking Manager', 'Booking Manager'
    EDITOR = 'Editor', 'Editor'
