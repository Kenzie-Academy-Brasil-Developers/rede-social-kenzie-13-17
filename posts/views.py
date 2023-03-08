from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Post
from users.models import User
from .serializers import PostSerializer
from django.shortcuts import get_object_or_404
from rest_framework.views import Response
from django.db.models import Q


class PostView(ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = PostSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["user"] = self.request.user
        return context

    def get_queryset(self):
        user = self.request.user
        following_posts = Post.objects.filter(user__in=User.objects.filter(followers=user))
        friend_posts = Post.objects.filter(user__in=User.objects.filter(friend_req=user, friendship_status=True))
        posts = following_posts.union(friend_posts)
        return posts
        # related_posts = Post.objects.filter(
        #     Q(user__in=user.followers.all()) | Q(user__friend_res=user, friendship_status=True)
        # )
        # return related_posts


class PostDetailView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = "id_post"

    def get_queryset(self):
        id_post = self.kwargs['id_post']
        instance = get_object_or_404(Post, pk=id_post)
        return instance

    def retrieve(self, request, *args, **kwargs):
        id_post = self.kwargs['id_post']
        instance = get_object_or_404(Post, pk=id_post)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def perform_destroy(self, instance):
        id_post = self.kwargs['id_post']
        instance = get_object_or_404(Post, pk=id_post)
        instance.delete()
