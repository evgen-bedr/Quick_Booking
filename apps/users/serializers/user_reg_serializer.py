import re
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from apps.users.models.user_model import User


class RegisterUserSerializer(serializers.ModelSerializer):
    re_password = serializers.CharField(max_length=40, write_only=True)

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "phone",
            "password",
            "re_password"
        ]
        extra_kwargs = {"password": {
            "write_only": True
        }}

    def validate(self, attrs):
        user_name = attrs.get('username')
        first_name = attrs.get('first_name').capitalize()
        last_name = attrs.get('last_name').capitalize()
        email = attrs.get('email')
        phone = attrs.get('phone')

        if not re.match('^[A-Za-z0-9_.]+$', user_name):
            raise serializers.ValidationError(
                {'user_name': 'The username must be alphanumeric characters or have only _ . symbols.'}
            )
        if not re.match('^[A-Za-z]+$', first_name):
            raise serializers.ValidationError(
                {'first_name': 'The first_name must be alphabet characters.'}
            )
        if not re.match('^[A-Za-z]+$', last_name):
            raise serializers.ValidationError(
                {'last_name': 'The last_name must be alphabet characters.'}
            )

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

        attrs['first_name'] = first_name
        attrs['last_name'] = last_name

        return attrs

    def create(self, validated_data):
        password = validated_data.get('password')
        validated_data.pop('re_password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()

        return user
