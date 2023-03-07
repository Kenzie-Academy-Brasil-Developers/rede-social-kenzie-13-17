from rest_framework import generics
from .serializer import UserSerializer
from .models import User
from rest_framework_simplejwt.authentication import JWTAuthentication


class UserView(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    # authentication_classes = JWTAuthentication
    serializer_class = UserSerializer
    queryset = User.objects.all()
