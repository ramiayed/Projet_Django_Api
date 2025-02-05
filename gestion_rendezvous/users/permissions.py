from rest_framework.permissions import BasePermission

class IsClient(BasePermission):
    """
    Permission pour les utilisateurs ayant le rôle de Client.
    """
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.groups.filter(name='Client').exists()
        )


class IsMechanic(BasePermission):
    """
    Permission pour les utilisateurs ayant le rôle de Mécanicien.
    """
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.groups.filter(name='Mechanic').exists()
        )
