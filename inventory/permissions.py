from rest_framework.permissions import BasePermission,SAFE_METHODS


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and ( request.user.is_superuser
            or request.user.groups.filter(name="ADMIN").exists()
            )
        )


class IsAdminOrSellerReadOnly(BasePermission):
   def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.user.is_superuser:
            return True

        if request.user.groups.filter(name="ADMIN").exists():
            return True

        if (
            request.user.groups.filter(name="SELLER").exists()
            and request.method in SAFE_METHODS
        ):
            return True

        return False