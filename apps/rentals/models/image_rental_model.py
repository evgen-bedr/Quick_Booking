from django.db import models
from apps.rentals.models.rental_model import Rental
import os


class Image(models.Model):
    rental = models.ForeignKey('Rental', related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/rental_images/')
    is_main = models.BooleanField(default=False)

    def __str__(self):
        return f"Image {self.id}"

    def delete(self, *args, **kwargs):
        # Удаление файла с диска
        if self.image and os.path.isfile(self.image.path):
            os.remove(self.image.path)
        super().delete(*args, **kwargs)
