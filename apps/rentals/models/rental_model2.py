from django.db import models
from django.conf import settings

from apps.rentals.choices.rental_choice import PropertyTypeChoices, TagChoices


class Rental(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    address = models.CharField(max_length=255)
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
    main_image = models.ImageField(upload_to='images/rental_images/', null=True, blank=True)
    additional_images = models.ManyToManyField('Image', related_name='rentals')
    views_count = models.IntegerField(default=0)
    contact_info = models.CharField(max_length=255, null=True, blank=True)
    verified = models.BooleanField(default=False)
    rejection_reason = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title

    def increment_views(self):
        self.views_count += 1
        self.save(update_fields=['views_count'])

    def save(self, *args, **kwargs):
        if self.pk:
            original = Rental.objects.get(pk=self.pk)
            if (self.title != original.title or
                    self.description != original.description or
                    self.address != original.address or
                    self.city != original.city or
                    self.country != original.country or
                    self.price != original.price or
                    self.rooms != original.rooms or
                    self.property_type != original.property_type or
                    self.tags != original.tags or
                    self.main_image != original.main_image or
                    self.availability_start_date != original.availability_start_date or
                    self.availability_end_date != original.availability_end_date):
                self.verified = False
        super().save(*args, **kwargs)


class Image(models.Model):
    rental = models.ForeignKey(Rental, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/rental_images/')

    def __str__(self):
        return f"Image {self.id}"
