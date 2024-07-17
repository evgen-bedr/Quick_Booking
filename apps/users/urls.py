from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.users.views.user_view_set import UserViewSet

router = DefaultRouter()
router.register(r'', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
]


# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
#
# from apps.users.views.user_reg_view import RegisterUserViewSet
# from apps.users.views.login_user_view import LoginUserView
# from apps.users.views.logout_user_view import LogoutUserView
#
# router = DefaultRouter()
# router.register(r'register', RegisterUserViewSet, basename='register')
# # router.register(r'login', LoginUserView, basename='login')
# # router.register(r'logout', LogoutUserView, basename='logout')
#
# urlpatterns = [
#     path('', include(router.urls)),
# ]

#
#
# from django.urls import path, include
# from apps.users.views.user_reg_view import RegisterUserView
# from routers.user_router import router
#
# from apps.users.views.login_user_view import LoginUserView, login_view
# from apps.users.views.logout_user_view import LogoutUserView
#
# urlpatterns = [
#
#     path('register/', RegisterUserView.as_view(), name='register'),
#     path('login/', login_view, name='login_page'),
#     path('login/api/', LoginUserView.as_view(), name='login'),
#     path('logout/', LogoutUserView.as_view(), name='logout'),
#     path('', include(router.urls)),
# ]
