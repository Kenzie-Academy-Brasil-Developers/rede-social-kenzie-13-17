from .models import Comment
from rest_framework.generics import ListCreateAPIView, UpdateAPIView, DestroyAPIView
from .serializers import CommentSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from posts.models import Post
from django.shortcuts import get_object_or_404
from .permissions import IsFriendOrFollowedBy, IsPostOrCommentOwner


class CommentsView(ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsFriendOrFollowedBy]

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        id_post = self.kwargs['id_post']
        comments = Comment.objects.filter(posts_id=id_post)
        return comments

    def perform_create(self, serializer):
        id_post = self.kwargs['id_post']
        get_object_or_404(Post, pk=id_post)
        serializer.save(posts_id=id_post)


class CommentsDetailView(UpdateAPIView, DestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsPostOrCommentOwner]

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_destroy(self, instance):
        id_comment = self.kwargs['id_comment']
        instance = get_object_or_404(Comment, id_comment)
        instance.delete()
