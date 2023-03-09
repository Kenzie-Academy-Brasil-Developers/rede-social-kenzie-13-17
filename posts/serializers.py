from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import Post
from users.serializer import UserSerializer
from users.models import User
from django.shortcuts import get_object_or_404
import ipdb

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'id',
            'user',
            'title',
            'content',
            'is_private',
            'created_at',
            'users_likes']
        read_only_fields = ['id', 'user', 'users_likes']

    def create(self, validated_data):
        validated_data['user'] = self.context['user']
        return super().create(validated_data)


class LikeSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    post_id = serializers.IntegerField(read_only=True)
    user = UserSerializer(read_only=True)

    def create(self, validated_data):
        print(validated_data)
        post_id = validated_data["post_id"]
        user = validated_data["user_id"]

        post = get_object_or_404(Post, pk=post_id)

        post.users_likes.add(user)
        
        return {}
    
    def to_representation(self, instance):
        return {'message': 'Like adicionado com sucesso!'}