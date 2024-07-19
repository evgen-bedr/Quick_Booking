from django.db import models
from django.conf import settings
from django.core.cache import cache
from django.utils import timezone
from datetime import timedelta
from django.db.models import F, ExpressionWrapper, FloatField
from django.db.models.functions import Coalesce

from apps.rentals.choices.rental_choice import PropertyTypeChoices


class RentalManager(models.Manager):
    def with_average_rating(self):
        return self.annotate(
            average_rating=ExpressionWrapper(
                Coalesce(F('ratings_sum'), 0) / Coalesce(F('ratings_count'), 1),
                output_field=FloatField()
            )
        )


class Rental(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    address = models.CharField(max_length=255)
    location = models.CharField(max_length=40, null=True, blank=True)
    city = models.CharField(max_length=40)
    country = models.CharField(max_length=40)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rooms = models.IntegerField()
    property_type = models.CharField(max_length=50, choices=PropertyTypeChoices.choices)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tags = models.ManyToManyField('Tag', related_name='rentals')
    availability_start_date = models.DateField(null=True, blank=True)
    availability_end_date = models.DateField(null=True, blank=True)
    additional_images = models.ManyToManyField('Image', related_name='rentals')
    views_count = models.IntegerField(default=0)
    contact_info = models.CharField(max_length=255, null=True, blank=True)
    ratings_sum = models.IntegerField(default=0)
    ratings_count = models.IntegerField(default=0)
    reviews_count = models.IntegerField(default=0)
    verified = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)
    rejection_reason = models.TextField(null=True, blank=True)

    objects = RentalManager()

    def __str__(self):
        return self.title

    def increment_views(self, user, ip_address):
        now = timezone.now()
        cache_key = f"rental_view_{self.id}_{user.id if user.is_authenticated else ip_address}"
        last_viewed = cache.get(cache_key)

        if not last_viewed or (now - last_viewed) > timedelta(seconds=10):
            self.views_count += 1
            self.save(update_fields=['views_count'])
            cache.set(cache_key, now, timeout=10)

    def get_average_rating(self):
        if self.ratings_count == 0:
            return 0
        return round(self.ratings_sum / self.ratings_count, 1)

    get_average_rating.short_description = 'Average Rating'
