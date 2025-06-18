from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdmin(BasePermission):
    """
    Allows access only to users with the vendor role.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'Admin'


class IsUser(BasePermission):
    """
    Allows access only to users with the User role.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'User'


class IsOwnerOrReadOnly(BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has a `vendor` or `customer` attribute.
    """
    def has_object_permission(self, request, view, obj):
        # Read-only permissions are allowed to any request
        if request.method in SAFE_METHODS:
            return True

        # Check object ownership
        if hasattr(obj, 'Admin'):
            return obj.vendor == request.user
        elif hasattr(obj, 'User'):
            return obj.customer == request.user
        return False
from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminOrReadOnlyForUser(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            # Admin: full access
            if request.user.role == 'Admin':
                return True
            # User: only safe methods
            elif request.user.role == 'User':
                return request.method in SAFE_METHODS
        return False
class IsBookingOwnerOrAdminReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.role == 'Admin':
            return request.method in SAFE_METHODS
        return obj.customer == request.user  # Only owner can access their own booking

    def has_permission(self, request, view):
        return request.user.is_authenticated
from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsReviewOwnerOrAdminReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Admins can only read
        if request.user.role == 'Admin':
            return request.method in SAFE_METHODS
        # Users can access their own reviews
        return obj.customer == request.user

    def has_permission(self, request, view):
        return request.user.is_authenticated
