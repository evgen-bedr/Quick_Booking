# apps/rentals/serializers/rental_serializer.py
from rest_framework import serializers
from apps.rentals.models.rental_model import Rental
from apps.rentals.serializers.image_serializer import ImageSerializer
from apps.rentals.models.tag_model import Tag

class RentalSerializer(serializers.ModelSerializer):
    additional_images = ImageSerializer(many=True, read_only=True, source='images')
    main_image = serializers.SerializerMethodField()
    tags = serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        queryset=Tag.objects.all()
    )
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Rental
        fields = [
            'id', 'title', 'description', 'address', 'location', 'city', 'country', 'price', 'rooms',
            'property_type', 'status', 'created_at', 'updated_at', 'user', 'tags',
            'availability_start_date', 'availability_end_date', 'main_image',
            'additional_images', 'views_count', 'contact_info', 'ratings_sum', 'ratings_count', 'average_rating',
            'verified', 'rejected', 'rejection_reason'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at', 'views_count', 'verified', 'rejection_reason']

    def create(self, validated_data):
        tags_data = validated_data.pop('tags', [])
        rental = Rental.objects.create(**validated_data)
        rental.tags.set(tags_data)

        # Обновляем роль пользователя
        self.update_user_role(rental.user)

        return rental

    def update(self, instance, validated_data):
        tags_data = validated_data.pop('tags', [])
        instance = super().update(instance, validated_data)

        if tags_data:
            for tag_name in tags_data:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                instance.tags.add(tag)

        # Обновляем роль пользователя
        self.update_user_role(instance.user)

        return instance

    def get_main_image(self, obj):
        main_image = obj.images.filter(is_main=True).first()
        if main_image:
            return {
                'id': main_image.id,
                'image': main_image.image.url
            }
        return None

    def get_average_rating(self, obj):
        return obj.get_average_rating()

    def update_user_role(self, user):
        active_rentals = user.rental_set.filter(status=True).exists()
        if active_rentals:
            user.role = 'Landlord'
        else:
            user.role = 'User'
        user.save(update_fields=['role'])
