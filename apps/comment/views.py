from django.shortcuts import render
from rest_framework import generics, permissions

from apps.comment.models import Comment
from apps.post.permissions import IsAuthorOrAdminOrPostOwner
from serializers import CommentSerializer


class CommentCreateView(generics.CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = permissions.IsAuthenticated,

    def perform_create(self, serializer):
        return serializer(owner=self.request.user)


class CommentDetailView(generics.RetrieveDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_permissions(self):
        if self.request.method == 'DELETE':
            return IsAuthorOrAdminOrPostOwner(),
        return permissions.AllowAny(),

