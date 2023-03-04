from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    Verify that the user requesting access to the resource is its author
    """
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
