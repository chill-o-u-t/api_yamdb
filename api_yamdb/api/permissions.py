from rest_framework import permissions


class IsSuperUserOrReadOnly(permissions.BasePermission):
    """ Пермишен для суперюзера джанго"""
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS or (
                request.user.is_authenticated
            )
        )

    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser


class IsAdminOrDefaultUser(permissions.BasePermission):
    """ Пермишен для прав модератор. """
    # Я пока не очень понял, где обозначается кто есть модератор

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS or (
                request.user.is_authenticated
            )
        )

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff



