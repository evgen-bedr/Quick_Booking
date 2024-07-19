from django.http import HttpResponseNotFound
from functools import wraps
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed


def moderator_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_superuser or (hasattr(request.user, 'role') and request.user.role == 'Moderator'):
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponseNotFound("Page not found.")

        jwt_authenticator = JWTAuthentication()
        try:
            auth_result = jwt_authenticator.authenticate(request)
            if auth_result is None:
                raise AuthenticationFailed('User not authenticated')
            user, validated_token = auth_result
            if not user.is_superuser and not (hasattr(user, 'role') and user.role == 'Moderator'):
                return HttpResponseNotFound("Page not found.")
        except AuthenticationFailed:
            return HttpResponseNotFound("Page not found.")

        return view_func(request, *args, **kwargs)

    return _wrapped_view
