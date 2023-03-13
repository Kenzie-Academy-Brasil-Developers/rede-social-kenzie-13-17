from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
)
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Post
from .serializers import PostSerializer, LikeSerializer
from django.shortcuts import get_object_or_404

from .serializers import PostSerializer
from .permissions import IsPostOwner
from django.http import Http404
from rest_framework.exceptions import ValidationError
from django.db.models import Q


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
        friendsreq = user.friend_req.filter(friendship_status=True).values_list(
            "user_relation", flat=True
        )
        friendsres = user.friend_res.filter(friendship_status=True).values_list(
            "user_relation", flat=True
        )
        following = user.following.all()
        return Post.objects.filter(
            Q(user=user)
            | Q(user__in=friendsreq)
            | Q(user__in=friendsres)
            | Q(user__in=following),
            is_private=False,
        ).distinct()


class PostDetailView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsPostOwner]

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = "id"


class LikeView(CreateAPIView, DestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Post.objects.all()
    serializer_class = LikeSerializer
    lookup_field = "id"

    def perform_create(self, serializer):
        print(self.request.user)
        post = self.kwargs.get("id")
        user = self.request.user
        post_obj = get_object_or_404(Post, id=post)

        if post_obj.users_likes.filter(id=user.id).exists():
            raise ValidationError("User already like this post")

        serializer.save(post_id=post, user_id=user.id)

    def perform_destroy(self, instance):
        post = get_object_or_404(Post, id=self.kwargs.get("id"))
        user = self.request.user
        post.users_likes.remove(user)


class FriendPostView(ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = PostSerializer

    lookup_field = "id_user"

    def get_queryset(self):
        query = Post.objects.filter(user_id=self.kwargs.get("id_user"))
        if query:
            return query
        raise Http404
