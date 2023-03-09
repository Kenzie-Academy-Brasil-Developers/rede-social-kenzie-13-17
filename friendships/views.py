from .models import Friendship
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    DestroyAPIView,
    UpdateAPIView,
)
from .serializers import FriendshipSerializer
from django.db.models import Q


class FriendshipView(ListAPIView):
    authentication_classes = [JWTAuthentication]

    serializer_class = FriendshipSerializer
    queryset = Friendship.objects.all()

    def get_queryset(self):
        return Friendship.objects.all().filter(
            Q(user_id=self.request.user.id) | Q(user_relation_id=self.request.user.id),
            friendship_status=True,
        )


class FriendshipPendingView(ListAPIView):
    authentication_classes = [JWTAuthentication]

    serializer_class = FriendshipSerializer
    queryset = Friendship.objects.all()

    def get_queryset(self):
        return self.request.user.friend_res.all().filter(friendship_status=False)


class FriendshipDetailView(CreateAPIView, UpdateAPIView, DestroyAPIView):
    authentication_classes = [JWTAuthentication]

    serializer_class = FriendshipSerializer
    queryset = Friendship.objects.all()
    lookup_url_kwarg = "id_user"

    def perform_create(self, serializer):
        serializer.save(
            user_id=self.request.user.id, user_relation_id=self.kwargs.get("id_user")
        )

    def partial_update(self, request, *args, **kwargs):
        new_friend_user = self.request.user.friend_res.all().get(
            user_id=kwargs["id_user"]
        )

        new_friend_user.friendship_status = True

        new_friend_user.save()

        return Response({"message": "new friendship created"}, status.HTTP_200_OK)
