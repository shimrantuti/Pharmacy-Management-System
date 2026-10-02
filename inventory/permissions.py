from rest_framework.permissions import BasePermission,SAFE_METHODS


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return  request.user.is_authenticated and ( request.user.is_superuser
            or request.user.groups.filter(name="ADMIN").exists()
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

class IsAdminOrSellerOrder(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.user.is_superuser:
            return request.method in ["GET", "POST", "PATCH"]

        if request.user.groups.filter(
            name__in=["ADMIN", "SELLER"]
        ).exists():
            return request.method in ["GET", "POST", "PATCH"]

        return False

    
class IsAdminOrSellerOrderItem(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.user.is_superuser:
            return True

        if request.user.groups.filter(
            name__in=["ADMIN", "SELLER"]
        ).exists():
            return True

        return False

    def has_object_permission(self, request, view, obj):
        # Anyone allowed by has_permission can GET
        if request.method in SAFE_METHODS:
            return True

        # Get the Order connected to this SalesOrderItem
        if obj.order.status == "COMPLETED":
            return False

        return True