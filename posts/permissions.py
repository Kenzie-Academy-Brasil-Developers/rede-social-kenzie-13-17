from rest_framework import permissions
from friendships.models import Friendship
from django.db.models import Q


class IsPostOrCommentOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return obj.user.id == request.user.id


class IsPrivatePost(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            if obj.is_private is False:
                return True
            elif obj.user.id == request.user.id:
                return True
            elif request.user.id in obj.user.followers:
                return True
            else:
                for friendship in Friendship.objects.filter(
                    Q(user_id=self.request.user.id) |
                    Q(user_relation_id=self.request.user.id),
                    friendship_status=True,
                ):
                    if (friendship.user_id == obj.user.id or
                            friendship.user_relation_id == obj.user.id):
                        return True
                return False
        else:
            return True
