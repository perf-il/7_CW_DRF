from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        return request.user == view.get_object().user
