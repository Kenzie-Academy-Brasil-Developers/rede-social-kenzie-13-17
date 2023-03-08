from rest_framework import generics
from .serializer import UserSerializer, FollowSerializer
from .models import User
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import get_object_or_404
import datetime
import ipdb


class UserView(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all().filter(is_active=True)


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    # authentication_classes = JWTAuthentication
    serializer_class = UserSerializer
    queryset = User.objects.all().filter(is_active=True)

    def perform_destroy(self, instance):
        instance.deleted_at = datetime.datetime.now()
        instance.is_active = False
        instance.save()


class UserFollowView(generics.CreateAPIView, generics.DestroyAPIView):
    authentication_classes = [JWTAuthentication]

    serializer_class = FollowSerializer
    queryset = User.objects.all()
    lookup_url_kwarg = "id_user"

    def perform_create(self, serializer):
        user_to_follow = get_object_or_404(User, pk=self.kwargs.get("id_user"))

        serializer.save(from_user_id=self.request.user.id, to_user_id=user_to_follow.id)

    def perform_destroy(self, instance):
        # pegando usuário que deixará de ser seguido
        user_to_unfollow = self.request.user.followers.all().get(pk=instance.id)

        # desfazendo relação, tem que arrumar pra desfazer somente uma
        user_to_unfollow.following.clear()


class UserFollowsView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]

    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_queryset(self):
        # nome deveria ser following?
        return self.request.user.followers.all()


class UserFollowersView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]

    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_queryset(self):
        # nome deveria ser followers?
        return self.request.user.following.all()
