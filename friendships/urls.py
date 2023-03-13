from django.urls import path
from .views import FriendshipView, FriendshipPendingView, FriendshipDetailView

urlpatterns = [
    path("friends/", FriendshipView.as_view()),
    path("friends/pending", FriendshipPendingView.as_view()),
    path("friend/<uuid:id_user>/", FriendshipDetailView.as_view()),
]
