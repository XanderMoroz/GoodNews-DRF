from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """Кастомный пермишн позволяющий вносить изменения только админам сайта."""
    def has_permission(self, request, view):
        # Если метод запроса GET, HEAD или OPTIONS.
        if request.method in permissions.SAFE_METHODS:
            # То ограничений нет.
            return True
        # В противном случае разрешение дается только админам сайта.
        return bool(request.user and request.user.is_staff)


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Кастомный пермишн позволяющий вносить изменения только владельцам объекта."""
    def has_object_permission(self, request, view, obj):
        # Если метод запроса GET, HEAD или OPTIONS
        if request.method in permissions.SAFE_METHODS:
            # То ограничений нет
            return True
        # В противном случае разрешение дается только владельцам объекта
        return obj.author == request.user
