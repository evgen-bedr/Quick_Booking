from rest_framework import serializers
from apps.rentals.models.image_rental_model import Image


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'image', 'is_main']
