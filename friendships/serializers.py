from rest_framework import serializers

from .models import Friendship


class FriendshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friendship
        fields = ["id", "friendship_status", "user_id", "user_relation_id"]
