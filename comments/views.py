from .models import Comment
from rest_framework.generics import ListCreateAPIView, UpdateAPIView, DestroyAPIView
from .serializers import CommentSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from posts.models import Post
from users.models import User
from django.shortcuts import get_object_or_404
from .permissions import IsFriendOrFollowed, IsPostOrCommentOwner


class CommentsView(ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsFriendOrFollowed]

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        id_post = self.kwargs['id_post']
<<<<<<< HEAD
        comments = Comment.objects.filter(publication=id_post)
=======
        comments = Comment.objects.filter(publication_id=id_post)
>>>>>>> 8e117fac0543d0e83da57fea06c177c88fd1cd26
        return comments

    def perform_create(self, serializer):
        id_post = self.kwargs['id_post']
<<<<<<< HEAD
        id_user = self.request.user.id
        post = get_object_or_404(Post, pk=id_post)
        user = get_object_or_404(User, pk=id_user)
        serializer.save(publication=post, user=user)
=======
        get_object_or_404(Post, pk=id_post)
        serializer.save(publication_id=id_post, user_id=self.request.user.id)
>>>>>>> 8e117fac0543d0e83da57fea06c177c88fd1cd26


class CommentsDetailView(UpdateAPIView, DestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsPostOrCommentOwner]

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_url_kwarg = "id_comment"
<<<<<<< HEAD

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def perform_destroy(self, instance):
        instance.delete()
=======
>>>>>>> 8e117fac0543d0e83da57fea06c177c88fd1cd26
