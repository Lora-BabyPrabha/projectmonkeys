from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsVendor(BasePermission):
    """
    Allows access only to users with the vendor role.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'vendor'


class IsCustomer(BasePermission):
    """
    Allows access only to users with the customer role.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'customer'


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
        if hasattr(obj, 'vendor'):
            return obj.vendor == request.user
        elif hasattr(obj, 'customer'):
            return obj.customer == request.user
        return False
