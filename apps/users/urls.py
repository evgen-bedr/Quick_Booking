from django.urls import path, include
from apps.users.views.user_reg_view import RegisterUserView
from routers.user_router import router

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('', include(router.urls)),
]