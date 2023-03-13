from rest_framework.generics import (ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView,
                                     CreateAPIView,
                                     DestroyAPIView,
                                     ListAPIView)
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Post
from .serializers import PostSerializer, LikeSerializer
from django.shortcuts import get_object_or_404
from .serializers import PostSerializer
from friendships.models import Friendship
from .permissions import IsPrivatePost, IsPostOwner, IsFriend
from rest_framework.exceptions import ValidationError


class PostView(ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsPrivatePost]

    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["user"] = self.request.user
        return context

    def get_queryset(self):
        user = self.request.user
        posts = Post.objects.filter(user__following=user)
        friends = Friendship.objects.filter(user_id=user.id, friendship_status=True)
        for obj in friends:
            id = obj.user_relation
            friend_post = Post.objects.filter(user_id=id)
            posts = posts.union(friend_post)

        return posts


class PostDetailView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsPostOwner]

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'id'


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
        post_obj = get_object_or_404(Post, id=post)

        if post_obj.users_likes.filter(id=user.id).exists():
            raise ValidationError('User already like this post')

        serializer.save(post_id=post, user_id=user.id)

    def perform_destroy(self, instance):
        post = get_object_or_404(Post, id=self.kwargs.get('id'))
        user = self.request.user
        post.users_likes.remove(user)


class FriendPostView(ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsFriend]

    serializer_class = PostSerializer

    lookup_field = 'id_user'

    def get_queryset(self):
        query = Post.objects.filter(user_id=self.kwargs.get('id_user'))
        return query
