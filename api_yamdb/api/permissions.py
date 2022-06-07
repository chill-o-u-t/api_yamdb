from rest_framework import permissions


class AuthorOrStaffPermission(permissions.BasePermission):
    """ Редактирование для автора, либо для стафа. """

    def has_object_permission(self, request, view, obj):
        if request.method not in permissions.SAFE_METHODS:
            return (
                obj.author == request.user
                or request.user.is_admin
                or request.user.is_moderator
                or request.user.is_superuser
                or request.user.is_staff
            )
        return True


class AdminPermission(permissions.BasePermission):
    """ Пермишен для прав модератор и админ. """
    """ Используется для вьюсетов: произведения, категории и жанры."""

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_admin
            or request.user.is_superuser
        )


class AdminOrReadOnlyPermission(permissions.BasePermission):
    """ Пермишен для прав модератор и админ. """
    """ Используется для вьюсетов: произведения, категории и жанры."""

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS or (
                request.user.is_authenticated
                and request.user.is_admin
                or request.user.is_superuser
            )
        )
