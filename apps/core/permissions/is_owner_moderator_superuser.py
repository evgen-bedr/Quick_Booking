# apps/core/permissions/is_owner_moderator_superuser.py
from rest_framework.permissions import BasePermission


class IsOwnerOrModeratorOrSuperUser(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
                request.user and
                (request.user.is_superuser or request.user.role == 'Moderator' or obj == request.user)
        )
