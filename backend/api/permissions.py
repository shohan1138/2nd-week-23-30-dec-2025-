from rest_framework.permissions import BasePermission

class IsAdminOrReadOnly(BasePermission):
    """
    Custom permission to only allow admin users to edit objects.
    Non-admin users can only read.
    """

    def has_permission(self, request, view):
        if request.method in ['GET']:
            return True
        return request.user and request.user.is_staff
