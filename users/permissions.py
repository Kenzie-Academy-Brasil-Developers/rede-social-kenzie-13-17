from rest_framework import permissions
from users.models import User
from rest_framework.views import View


class IsReqUser(permissions.BasePermission):
    def has_object_permission(self, request, view: View, obj: User) -> bool:
        return obj.id == request.user.id
