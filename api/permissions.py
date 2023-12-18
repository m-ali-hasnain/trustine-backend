from rest_framework import permissions
import re
from .constants import ADMIN, STUDENT
from .utils import in_restricted_paths

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow read access to anyone, but restrict write access to admin users.
    """ 
    restricted_paths = [r'/api/courses/\d+/students', r'/api/registrations']

    def has_permission(self, request, view):
        # Allow read access for everyone (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS and not in_restricted_paths(self.restricted_paths, request.path):
            return True

        # Restrict write access to admin users for other methods (POST, PUT, DELETE)
        return request.user and request.user.is_authenticated and request.user.role == ADMIN

class IsStudent(permissions.BasePermission):
   
    restricted_paths = [r'/api/courses/\d+/students', r'/api/registrations']
    
    def has_permission(self, request, view):
        # Allow read access for everyone (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS and not in_restricted_paths(self.restricted_paths, request.path):
            return True

        # Restrict write access to student users for other methods (POST, PUT, DELETE)
        return request.user and request.user.is_authenticated and request.user.role == STUDENT
