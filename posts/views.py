from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView, DestroyAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Post
from users.models import User
from .serializers import PostSerializer, LikeSerializer
from django.shortcuts import get_object_or_404
from rest_framework.views import Response
from django.db.models import Q
from .serializers import PostSerializer
from friendships.models import Friendship


class PostView(ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["user"] = self.request.user
        return context

    def get_queryset(self):
        user = self.request.user
        posts = Post.objects.filter(user__followers=user)
        friends = Friendship.objects.filter(user_id=user.id)
        for x in friends:
            id = x.user_relation
            friend_post = Post.objects.filter(user_id=id)
            posts = posts.union(friend_post)

        return posts


class PostDetailView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = "id"


class LikeView(CreateAPIView, DestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()
    serializer_class = LikeSerializer
    lookup_field = 'id'

    def perform_create(self, serializer):
        print(self.request.user)
        post = self.kwargs.get('id')
        user = self.request.user
        serializer.save(post_id=post, user_id=user.id)
        return Response({'message': 'Like adicionado com sucesso!'})

    def perform_destroy(self, instance):
        post = get_object_or_404(Post, id=self.kwargs.get('id'))
        user = self.request.user
        post.users_likes.remove(user)
