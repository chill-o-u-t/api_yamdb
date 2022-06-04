from rest_framework import permissions


class IsSuperUserOrReadOnly(permissions.BasePermission):
    """ Пермишен для суперюзера джанго"""

    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser


class AuthorOrStaffPermission(permissions.BasePermission):
    """ Редактирование для автора, либо для стафа: комента и ревью. """

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user or request.user.role == 'admin'


class AdminPermission(permissions.BasePermission):
    """ Пермишен для прав модератор и админ. """
    """ Используется для вьюсетов: произведения, категории и жанры."""

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == 'admin'
        )
