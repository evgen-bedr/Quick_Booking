# apps/rentals/serializers/rental_serializer.py
from rest_framework import serializers
from apps.rentals.models.rental_model import Rental
from apps.rentals.serializers.image_serializer import ImageSerializer
from apps.rentals.models.tag_model import Tag


class RentalSerializer(serializers.ModelSerializer):
    additional_images = ImageSerializer(many=True, read_only=True)
    tags = serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        queryset=Tag.objects.all()
    )

    class Meta:
        model = Rental
        fields = [
            'title', 'description', 'address', 'city', 'country', 'price', 'rooms',
            'property_type', 'status', 'created_at', 'updated_at', 'user', 'tags',
            'availability_start_date', 'availability_end_date', 'main_image',
            'additional_images', 'views_count', 'contact_info', 'verified', 'rejection_reason'
        ]
        read_only_fields = ['user', 'created_at', 'updated_at', 'views_count', 'verified', 'rejection_reason']

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user if request else None
        tags_data = validated_data.pop('tags', [])
        rental = Rental(**validated_data)
        rental.user = user
        rental.save()
        rental.tags.set(tags_data)
        return rental

    def update(self, instance, validated_data):
        tags_data = validated_data.pop('tags', [])
        instance = super().update(instance, validated_data)
        if tags_data:
            instance.tags.set(tags_data)
        return instance
