from django.urls import path, include
from apps.users.views.user_reg_view import RegisterUserView
from routers.user_router import router

from apps.users.views.login_user_view import LoginUserView
from apps.users.views.logout_user_view import LogoutUserView

urlpatterns = [

    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', LogoutUserView.as_view(), name='logout'),
    path('', include(router.urls)),
]
