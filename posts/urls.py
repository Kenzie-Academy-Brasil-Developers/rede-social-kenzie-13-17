from django.urls import path
from .views import PostView, PostDetailView
from comments.views import CommentsView, CommentsDetailView

urlpatterns = [
    path("post/", PostView.as_view()),
    path("post/<id_post>/", PostDetailView.as_view()),
    path("post/<id_post>/comments/", CommentsView.as_view()),
    path("comments/<id_comment>/", CommentsDetailView.as_view()),
    # path("/post/<id_post>/like/", PostLikeView.as_view()),
]
