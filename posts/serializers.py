from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'id',
            'user',
            'title',
            'content',
            'is_private',
            'created_at']
        read_only_fields = ['id', 'user']

    def create(self, validated_data):
        validated_data['user'] = self.context['user']
        return super().create(validated_data)
