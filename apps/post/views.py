from rest_framework import generics
from rest_framework import permissions
from .models import Post
from .serializers import PostListSerializer, PostCreateSerializer


class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = PostListSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return  PostListSerializer
        return PostCreateSerializer






