from .models import Comment
from rest_framework.generics import ListCreateAPIView, UpdateAPIView, DestroyAPIView
from .serializers import CommentSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from publications.models import Publication
from django.shortcuts import get_object_or_404
from .permissions import IsFriendOrFollowed, IsPostOrCommentOwner


class CommentsView(ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsFriendOrFollowed]

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        id_post = self.kwargs['id_post']
        comments = Comment.objects.filter(publications_id=id_post)
        return comments

    def perform_create(self, serializer):
        id_post = self.kwargs['id_post']
        get_object_or_404(Publication, pk=id_post)
        serializer.save(publications_id=id_post)


class CommentsDetailView(UpdateAPIView, DestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsPostOrCommentOwner]

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)
    
    def perform_destroy(self, instance):
        instance.delete()
    

