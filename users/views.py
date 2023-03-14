from rest_framework import generics
from .serializer import UserSerializer, FollowSerializer
from .models import User
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import get_object_or_404
import datetime
from rest_framework.permissions import IsAuthenticated
import rest_framework.serializers as serializers
import uuid
from .permissions import IsReqUser


class UserView(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.filter(is_active=True)


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsReqUser]

    serializer_class = UserSerializer
    queryset = User.objects.filter(is_active=True)

    def perform_destroy(self, instance):
        instance.deleted_at = datetime.datetime.now()
        instance.is_active = False
        instance.save()


class UserFollowView(generics.CreateAPIView, generics.DestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = FollowSerializer
    queryset = User.objects.all()
    lookup_url_kwarg = "id_user"

    def perform_create(self, serializer):
        try:
            id_user = uuid.UUID(str(self.kwargs.get("id_user")))
        except ValueError:
            raise serializers.ValidationError({"message": "Invalid UUID"})

        user_to_follow = get_object_or_404(User, pk=id_user)

        serializer.save(from_user_id=self.request.user.id, to_user_id=user_to_follow.id)

    def perform_destroy(self, instance):
        user_to_unfollow = self.request.user.following.all().get(pk=instance.id)

        user_to_unfollow.followers.set(
            user_to_unfollow.followers.exclude(id=self.request.user.id)
        )


class UserFollowsView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_queryset(self):
        return self.request.user.following.all()


class UserFollowersView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_queryset(self):
        return self.request.user.followers.all()
