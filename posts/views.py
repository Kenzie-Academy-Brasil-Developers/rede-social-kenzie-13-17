from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Post
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
