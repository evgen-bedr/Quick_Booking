from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from apps.users.models.user_model import User
from apps.users.serializers.user_reg_serializer import RegisterUserSerializer

from apps.users.utils.set_jwt_cookies import set_jwt_cookies


class RegisterUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterUserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            headers = self.get_success_headers(serializer.data)
            response = Response(
                {"message": "Your registration was successful."},
                status=status.HTTP_201_CREATED,
                headers=headers
            )
            return response
            set_jwt_cookies(response, user)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
