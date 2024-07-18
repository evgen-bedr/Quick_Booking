# apps/rentals/models/tag_model.py
from django.db import models

from apps.rentals.choices.rental_choice import TagChoices


class Tag(models.Model):
    name = models.CharField(max_length=50, choices=TagChoices.choices, unique=True)

    def __str__(self):
        return self.name
