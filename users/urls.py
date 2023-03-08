from django.urls import path
from . import views
from rest_framework_simplejwt import views as jwt_views


urlpatterns = [
    path("login/", jwt_views.TokenObtainPairView.as_view()),
    path("users/", views.UserView.as_view()),
    path("users/<pk>/", views.UserDetailView.as_view()),
    path("follow/<id_user>/", views.UserFollowView.as_view()),
    path("follows/", views.UserFollowsView.as_view()),
    path("followers/", views.UserFollowersView.as_view()),
]
