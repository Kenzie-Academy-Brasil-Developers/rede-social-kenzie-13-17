from rest_framework import permissions
from friendships.models import Friendship
from django.db.models import Q
from rest_framework.exceptions import PermissionDenied


class IsPostOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return obj.user.id == request.user.id


class IsPrivatePost(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            user_id = request.user.id
            friend_id = request.resolver_match.kwargs.get('id_user')
            if obj.is_private is False:
                return True
            elif friend_id == user_id:
                return True
            elif request.user in obj.user.followers.all():
                return True
            else:
                try:
                    Friendship.objects.get(
                        Q(user_id=user_id, user_relation_id=friend_id, friendship_status=True) | 
                        Q(user_id=friend_id, user_relation_id=user_id, friendship_status=True)
                    )
                except Friendship.DoesNotExist:
                    raise PermissionDenied
                return False
        else:
            return True


class IsFriend(permissions.BasePermission):
    def has_permission(self, request, view) -> bool:
        if request.method in permissions.SAFE_METHODS:
            user_id = request.user.id
            friend_id = request.resolver_match.kwargs.get('id_user')
            if user_id == friend_id:
                return True
            try:
                Friendship.objects.get(
                    Q(user_id=user_id, user_relation_id=friend_id, friendship_status=True) | 
                    Q(user_id=friend_id, user_relation_id=user_id, friendship_status=True)
                )
            except Friendship.DoesNotExist:
                raise PermissionDenied
            return True
