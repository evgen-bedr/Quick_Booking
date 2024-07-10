from rest_framework import viewsets
from apps.users.models.user_model import User
from apps.users.serializers.user_serializer import UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
