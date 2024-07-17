# apps/core/permissions/moderator_or_super.py
from rest_framework.permissions import BasePermission


class IsModeratorOrSuperUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and (request.user.is_superuser or request.user.role == 'Moderator')
