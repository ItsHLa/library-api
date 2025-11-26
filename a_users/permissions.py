from rest_framework.permissions import BasePermission

class IsAuthenticated(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated)
    
class AllowAny(BasePermission):
    def has_permission(self, request, view):
        return True
    
class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_admin