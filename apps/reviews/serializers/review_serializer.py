# apps/reviews/serializers/review_serializer.py

from rest_framework import serializers
from apps.reviews.models.review_model import Review

class ReviewSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = ['id', 'user', 'username', 'rental', 'booking', 'rating', 'comment', 'status', 'created_at', 'updated_at']
        read_only_fields = ['user', 'username', 'rental', 'booking', 'status', 'created_at', 'updated_at']
        extra_kwargs = {
            'rating': {'required': False},
            'comment': {'required': False}
        }

    def get_username(self, obj):
        return obj.user.username
