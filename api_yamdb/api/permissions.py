from rest_framework import permissions


class SomebodyOrSomething(permissions.BasePermission):

    def has_permission(self, request, view):
        pass


class AdminOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_admin
        )
