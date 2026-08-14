from rest_framework.permissions import BasePermission


class IsSuperAdmin(BasePermission):
    """
    Super Admin can create, update and delete master data.
    Other authenticated users can only read master data.
    """

    def has_permission(self, request, view):

        # User must be authenticated
        if not request.user or not request.user.is_authenticated:
            return False

        # GET, HEAD and OPTIONS are allowed for all authenticated users
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
           return request.user.role == 'SA'

        # Write operations are restricted to Super Admin
        return request.user.role == 'SA'