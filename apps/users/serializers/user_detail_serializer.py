# apps/users/serializers/user_detail_serializer.py
from rest_framework import serializers
from apps.users.models.user_model import User


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'phone',
            'is_staff',
            'is_active',
            'role',
            'date_joined'
        ]
