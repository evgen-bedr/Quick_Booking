from django.urls import path, include
from apps.users.views.user_reg_view import RegisterUserView
from routers.user_router import router

from apps.users.views.login_user_view import LoginUserView, login_view
from apps.users.views.logout_user_view import LogoutUserView

urlpatterns = [

    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', login_view, name='login_page'),
    path('login/api/', LoginUserView.as_view(), name='login'),
    path('logout/', LogoutUserView.as_view(), name='logout'),
    path('', include(router.urls)),
]
