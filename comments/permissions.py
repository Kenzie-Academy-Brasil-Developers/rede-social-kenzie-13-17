from rest_framework import permissions
from .models import User
from rest_framework.views import View


class IsFriendOrFollowedBy(permissions.BasePermission):
    def has_object_permission(self, request, view: View, obj: User) -> bool:
        ...


class IsPostOrCommentOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        ...
