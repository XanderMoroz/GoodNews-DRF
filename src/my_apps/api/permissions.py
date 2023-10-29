from rest_framework import permissions

from src.my_apps.blogs.models import Author


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        current_author = Author.objects.filter(user=request.user).first()

        return obj.author == current_author