from rest_framework import serializers
from apps.reviews.models.review_model import Review


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'user', 'rental', 'booking', 'rating', 'comment', 'created_at', 'updated_at']
        read_only_fields = ['user', 'rental', 'booking', 'created_at', 'updated_at']
        extra_kwargs = {
            'rating': {'required': False},
            'comment': {'required': False}
        }
