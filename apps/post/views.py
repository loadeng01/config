from rest_framework import generics
from rest_framework import permissions
from .models import Post
from .serializers import PostListSerializer


class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = PostListSerializer

    # def get_serializer_class(self):
    #     if self.request.method == 'GET':
    #         return  PostListSerializer
    #     return PostCreateSerializer






