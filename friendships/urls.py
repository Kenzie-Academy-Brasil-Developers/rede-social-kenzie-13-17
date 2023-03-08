from django.urls import path
from .views import FriendshipView, FriendshipDetailView

urlpatterns = [
    path("friends/", FriendshipView.as_view()),
    path("friend/<id_user>/", FriendshipDetailView.as_view()),
]
