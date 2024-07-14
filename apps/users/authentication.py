from rest_framework_simplejwt.authentication import JWTAuthentication
from django.utils import timezone


class CustomJWTAuthentication(JWTAuthentication):

    def get_user(self, validated_token):
        user = super().get_user(validated_token)
        user.last_login = timezone.now()
        user.save(update_fields=['last_login'])
        return user
