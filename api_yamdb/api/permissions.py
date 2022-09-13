from rest_framework import permissions


class SomebodyOrSomething(permissions.BasePermission):

    def has_permission(self, request, view):
        pass
