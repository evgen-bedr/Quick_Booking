from rest_framework import serializers
from apps.rentals.models.tag_model import Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['name']
