from rest_framework.permissions import BasePermission, SAFE_METHODS

from exchanges.models import Exchange


class IsUpdateAllowed(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or obj.state == Exchange.State.PENDING