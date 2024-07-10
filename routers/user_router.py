from rest_framework.routers import DefaultRouter
from apps.users.views.user_view_set import UserViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)