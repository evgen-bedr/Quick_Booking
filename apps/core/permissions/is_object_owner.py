# apps/core/permissions/is_object_owner.py
from rest_framework.permissions import BasePermission


class IsObjectOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user and obj == request.user
