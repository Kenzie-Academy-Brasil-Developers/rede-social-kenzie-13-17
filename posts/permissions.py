from rest_framework import permissions
from rest_framework.views import View
from friendships.models import Friendship
from rest_framework.exceptions import PermissionDenied
from django.db.models import Q


class IsFriend(permissions.BasePermission):
    def has_permission(self, request, view: View) -> bool:
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
