from rest_framework import serializers
from .models import User
from django.shortcuts import get_object_or_404


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
            "is_active",
            "deleted_at",
            "updated_at",
            "date_joined",
            "followers",
            "following",
        ]

        extra_kwargs = {
            "password": {"write_only": True},
            "deleted_at": {"read_only": True},
            "updated_at": {"read_only": True},
            "followers": {"read_only": True, "many": True},
            "following": {"read_only": True},
            "first_name": {"required": True},
            "last_name": {"required": True},
        }

    def create(self, validated_data: dict) -> User:

        return User.objects.create_user(**validated_data)

    def update(self, instance: User, validated_data: dict) -> User:

        password = validated_data.pop("password", None)
        if password:
            instance.set_password(password)

        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance


class FollowSerializer(serializers.Serializer):
    from_user = UserSerializer(many=True, read_only=True)
    to_user = UserSerializer(many=True, read_only=True)

    def create(self, validated_data):
        follower_user = get_object_or_404(User, pk=validated_data["from_user_id"])

        follower_user.following.add(validated_data["to_user_id"])

        return {}
