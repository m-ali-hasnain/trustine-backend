from rest_framework import permissions
import re
from .constants import ADMIN, STUDENT
from .utils import in_restricted_paths

class BasePermissionWithRead(permissions.BasePermission):
    """
    Base permission class for read access.
    """
    restricted_paths = [r'/api/courses/\d+/students', r'/api/registrations']

    def has_read_permission(self, request):
        """
        Check read access for GET, HEAD, OPTIONS requests.
        """
        return request.method in permissions.SAFE_METHODS and not in_restricted_paths(self.restricted_paths, request.path)

class IsAdminOrReadOnly(BasePermissionWithRead):
    """
    Custom permission to allow read access to anyone, but restrict write access to admin users.
    """
    def has_permission(self, request, view):
        # Allow read access for everyone
        if self.has_read_permission(request):
            # Check if the user ID in the route matches the ID of the currently logged-in user
            if re.match(r'/users/\d+/courses/', request.path):
                return int(view.kwargs.get('pk')) == request.user.id
            else:
                return True

        # Restrict write access to admin users for other methods (POST, PUT, DELETE)
        return request.user and request.user.is_authenticated and request.user.role == ADMIN


class IsStudentOrReadOnly(BasePermissionWithRead):
    """
    Custom permission to allow read access to anyone, but restrict write access to student users.
    """
    def has_permission(self, request, view):
        # Allow read access for everyone
        if self.has_read_permission(request):
            return True

        # Restrict write access to student users for other methods (POST, PUT, DELETE)
        return request.user and request.user.is_authenticated and request.user.role == STUDENT
