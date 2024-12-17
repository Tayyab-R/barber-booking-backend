from rest_framework import permissions

class IsShopOwner(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and hasattr(request.user, 'owner_profile')

        
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and hasattr(request.user, 'owner_profile') and obj.owner == request.user.owner_profile
        
        
class IsBarber(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and hasattr(request.user, 'barber_profile')
    
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and hasattr(request.user, 'barber_profile') and obj.owner == request.user.barber_profile
        
