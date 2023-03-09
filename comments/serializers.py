from rest_framework import serializers
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ['id', 'comment', 'created_at', 'user', 'publication']
        read_only_fields = ['id', 'created_at', 'publication']

    def create(self, validated_data):
        return Comment.objects.create(**validated_data)

    def update(self, instance: Comment, validated_data: dict) -> Comment:
        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance
