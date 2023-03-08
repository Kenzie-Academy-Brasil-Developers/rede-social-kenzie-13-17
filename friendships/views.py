from .models import Friendship
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.generics import ListAPIView, CreateAPIView, DestroyAPIView
from .serializers import FriendshipSerializer
import ipdb


class FriendshipView(ListAPIView):
    authentication_classes = [JWTAuthentication]

    serializer_class = FriendshipSerializer
    queryset = Friendship.objects.all()

    def get_queryset(self):
        friends = Friendship.objects.all()

        return friends


class FriendshipDetailView(CreateAPIView, DestroyAPIView):
    authentication_classes = [JWTAuthentication]

    serializer_class = FriendshipSerializer

    def perform_create(self, serializer):
        serializer.save(
            user_id=self.request.user.id, user_relation_id=self.kwargs.get("id_user")
        )
