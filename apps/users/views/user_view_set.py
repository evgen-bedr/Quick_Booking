from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from datetime import datetime
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action

from apps.users.models.user_model import User
from apps.users.serializers.user_reg_serializer import RegisterUserSerializer
from apps.users.serializers.update_user_serializer import UpdateUserSerializer
from apps.users.serializers.user_detail_serializer import UserDetailSerializer
from apps.users.utils.set_jwt_cookies import set_jwt_cookies
from apps.core.permissions.moderator_or_super import IsModeratorOrSuperUser
from apps.core.permissions.is_owner_moderator_superuser import IsOwnerOrModeratorOrSuperUser
from apps.core.permissions.is_object_owner import IsObjectOwner

class UserViewSet(viewsets.ModelViewSet):
    pagination_class = PageNumberPagination  # Добавляем пагинацию

    def get_queryset(self):
        return User.objects.all().order_by('-date_joined')  # Упорядочение по дате регистрации

    def get_serializer_class(self):
        if self.action in ['create', 'register']:
            return RegisterUserSerializer
        elif self.action in ['update', 'partial_update']:
            return UpdateUserSerializer
        return UserDetailSerializer  # Default to UserDetailSerializer for other actions

    def get_permissions(self):
        if self.action in ['register', 'login', 'logout']:
            self.permission_classes = [AllowAny]
        elif self.action in ['update', 'partial_update']:
            self.permission_classes = [IsObjectOwner]
        elif self.action in ['retrieve']:
            self.permission_classes = [IsOwnerOrModeratorOrSuperUser]
        else:
            self.permission_classes = [IsModeratorOrSuperUser]
        return super().get_permissions()

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            headers = self.get_success_headers(serializer.data)

            # Создание токенов для нового пользователя
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            response = Response(
                {"message": "Your registration was successful."},
                status=status.HTTP_201_CREATED,
                headers=headers
            )

            # Установка токенов в куки
            response.set_cookie(
                key='access_token',
                value=access_token,
                httponly=True,
                secure=False,  # Установите True для HTTPS
                samesite='Lax',
                expires=datetime.fromtimestamp(refresh.access_token['exp']),
            )
            response.set_cookie(
                key='refresh_token',
                value=refresh_token,
                httponly=True,
                secure=False,  # Установите True для HTTPS
                samesite='Lax',
                expires=datetime.fromtimestamp(refresh['exp']),
            )
            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def login(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        if not email or not password:
            return Response(
                {"message": "Both email and password are required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        user = authenticate(request, username=email, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
            response = Response(
                {"message": f"Welcome back, {user.username}."},
                status=status.HTTP_200_OK
            )
            response.set_cookie(
                key='access_token',
                value=access_token,
                httponly=True,
                secure=False,  # Установите True для HTTPS
                samesite='Lax',
                expires=datetime.fromtimestamp(refresh.access_token['exp']),
            )
            response.set_cookie(
                key='refresh_token',
                value=refresh_token,
                httponly=True,
                secure=False,  # Установите True для HTTPS
                samesite='Lax',
                expires=datetime.fromtimestamp(refresh['exp']),
            )
            return response
        else:
            return Response(
                {"message": "Invalid email or password"},
                status=status.HTTP_401_UNAUTHORIZED
            )

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def logout(self, request):
        try:
            refresh_token = request.COOKIES.get('refresh_token')
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception:
            pass  # Token is invalid or already blacklisted

        response = Response(
            {"message": "Logout successful."},
            status=status.HTTP_204_NO_CONTENT
        )
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        return response

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        data = request.data.copy()
        data.pop('username', None)  # Удалить поле 'username' из данных для обновления

        serializer = self.get_serializer(instance, data=data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)

            # Вернуть только обновленные поля
            updated_fields = {field: value for field, value in serializer.validated_data.items() if field in data}
            return Response(updated_fields)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        serializer = self.get_serializer(instance)
        return Response(serializer.data)
