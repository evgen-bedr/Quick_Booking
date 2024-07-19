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
from apps.core.permissions.moderator_or_super import IsModeratorOrSuperUser
from apps.core.permissions.is_owner_moderator_superuser import IsOwnerOrModeratorOrSuperUser
from apps.core.permissions.is_object_owner import IsObjectOwner


class UserViewSet(viewsets.ModelViewSet):
    """
   Handles CRUD operations for user accounts.

   @pagination_class: PageNumberPagination : Pagination class used by the viewset
   """
    pagination_class = PageNumberPagination

    def get_queryset(self):
        """
        Retrieve the queryset of users, ordered by the date they joined.

        @param self: UserViewSet : Instance of the viewset

        @return: QuerySet : Users ordered by date joined
        """

        return User.objects.all().order_by('-date_joined')

    def get_serializer_class(self):
        """
        Return the appropriate serializer class based on the action being performed.

        @param self: UserViewSet : Instance of the viewset

        @return: Serializer : Serializer class based on action
        """
        if self.action in ['create', 'register']:
            return RegisterUserSerializer
        elif self.action in ['update', 'partial_update']:
            return UpdateUserSerializer
        return UserDetailSerializer

    def get_permissions(self):
        """
        Return the appropriate permissions based on the action being performed.

        @param self: UserViewSet : Instance of the viewset

        @return: List : List of permissions
        """
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
        """
        Handle user registration.

        @param request: Request : Request object containing registration data

        @return: Response : JSON response with registration success message or errors
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            headers = self.get_success_headers(serializer.data)

            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            response = Response(
                {"message": "Your registration was successful."},
                status=status.HTTP_201_CREATED,
                headers=headers
            )

            response.set_cookie(
                key='access_token',
                value=access_token,
                httponly=True,
                secure=False,
                samesite='Lax',
                expires=datetime.fromtimestamp(refresh.access_token['exp']),
            )
            response.set_cookie(
                key='refresh_token',
                value=refresh_token,
                httponly=True,
                secure=False,
                samesite='Lax',
                expires=datetime.fromtimestamp(refresh['exp']),
            )
            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def login(self, request):
        """
        Handle user login.

        @param request: Request : Request object containing login data

        @return: Response : JSON response with login success message and tokens or error message
        """
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
                secure=False,
                samesite='Lax',
                expires=datetime.fromtimestamp(refresh.access_token['exp']),
            )
            response.set_cookie(
                key='refresh_token',
                value=refresh_token,
                httponly=True,
                secure=False,
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
        """
        Handle user logout.

        @param request: Request : Request object

        @return: Response : JSON response confirming logout
        """
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
        """
        Update user account details.

        @param request: Request : Request object containing updated data
        @param args: tuple : Additional positional arguments
        @param kwargs: dict : Additional keyword arguments

        @return: Response : JSON response with updated fields or errors
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        data = request.data.copy()
        data.pop('username', None)

        serializer = self.get_serializer(instance, data=data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)

            updated_fields = {field: value for field, value in serializer.validated_data.items() if field in data}
            return Response(updated_fields)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a specific user account.

        @param request: Request : Request object
        @param args: tuple : Additional positional arguments
        @param kwargs: dict : Additional keyword arguments

        @return: Response : JSON response with user details
        """
        instance = self.get_object()

        serializer = self.get_serializer(instance)
        return Response(serializer.data)
