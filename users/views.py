from rest_framework import generics
from .serializer import UserSerializer
from .models import User
from rest_framework_simplejwt.authentication import JWTAuthentication
import datetime


class UserView(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.filter(is_active=True)


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    # authentication_classes = JWTAuthentication
    serializer_class = UserSerializer
    queryset = User.objects.filter(is_active=True)

    def perform_destroy(self, instance):
        instance.deleted_at = datetime.datetime.now()
        instance.is_active = False
        instance.save()
