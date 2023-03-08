from rest_framework import permissions
from users.models import User
from rest_framework.views import View


class IsFriendOrFollowed(permissions.BasePermission):
    def has_object_permission(self, request, view: View, obj: User) -> bool:
        return True


class IsPostOrCommentOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return True
