from rest_framework import permissions


class IsSuperUser(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class IsSuperUserOrReadOnly(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS or bool(
            super().has_permission(request, view) and request.user.is_superuser
        )

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)
