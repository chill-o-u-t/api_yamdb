from rest_framework import permissions


class AuthorOrStaffPermission(permissions.BasePermission):
    """ Редактирование для автора, либо для стафа: комента и ревью. """

    def has_object_permission(self, request, view, obj):
        if request.method not in permissions.SAFE_METHODS:
            return (
                obj.author == request.user or request.user.is_staff
            )
        return True


class AdminPermission(permissions.BasePermission):
    """ Пермишен для прав модератор и админ. """
    """ Используется для вьюсетов: произведения, категории и жанры."""

    def has_permission(self, request, view):
        return (
            request.user.is_superuser
            or request.user.is_authenticated
            and request.user.is_admin
        )


class SuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser
