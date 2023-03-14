from rest_framework import permissions
from users.models import User
from rest_framework.views import View


class IsReqUser(permissions.BasePermission):
    def has_object_permission(self, request, view: View, obj: User) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return obj.id == request.user.id
