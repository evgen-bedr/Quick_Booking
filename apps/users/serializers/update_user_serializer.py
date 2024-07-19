import re
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from apps.users.models.user_model import User


class UpdateUserSerializer(serializers.ModelSerializer):
    re_password = serializers.CharField(max_length=40, write_only=True, required=False)

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone",
            "password",
            "re_password"
        ]
        extra_kwargs = {
            "password": {"write_only": True, "required": False},
            "re_password": {"write_only": True, "required": False},
        }

    def validate(self, attrs):
        first_name = attrs.get('first_name')
        last_name = attrs.get('last_name')
        email = attrs.get('email')
        phone = attrs.get('phone')

        if first_name and not re.match('^[A-Za-z]+$', first_name):
            raise serializers.ValidationError(
                {'first_name': 'The first_name must be alphabet characters.'}
            )
        if last_name and not re.match('^[A-Za-z]+$', last_name):
            raise serializers.ValidationError(
                {'last_name': 'The last_name must be alphabet characters.'}
            )

        if email:
            try:
                validate_email(email)
            except ValidationError:
                raise serializers.ValidationError(
                    {'email': 'Enter a valid email address.'}
                )

        if phone and not re.match(r'^\+\d{1,3}\d{4,14}(?:x\d+)?$', phone):
            raise serializers.ValidationError(
                {'phone': 'Enter a valid phone number in the format +(country code) number.'}
            )

        password = attrs.get('password')
        re_password = attrs.get('re_password')

        if password or re_password:
            if password != re_password:
                raise serializers.ValidationError(
                    {'password': 'Passwords are not the same.'}
                )

            if len(password) < 7:
                raise serializers.ValidationError(
                    {'password': 'Password must be at least 7 characters long.'}
                )

            if not re.search(r'[A-Z]', password):
                raise serializers.ValidationError(
                    {'password': 'Password must contain at least one uppercase letter.'}
                )

            if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
                raise serializers.ValidationError(
                    {'password': 'Password must contain at least one special character.'}
                )

            try:
                validate_password(password)
            except ValidationError as err:
                raise serializers.ValidationError(
                    {'password': err.messages}
                )

        return attrs

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        validated_data.pop('re_password', None)
        if password:
            instance.set_password(password)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
