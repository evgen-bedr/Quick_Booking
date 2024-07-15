from rest_framework.permissions import BasePermission


class IsModeratorOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
                request.user.is_superuser or
                (hasattr(request.user, 'role') and request.user.role == 'Moderator')
        )
