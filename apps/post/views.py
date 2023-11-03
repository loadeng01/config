# from rest_framework import generics
# from rest_framework import permissions
# from .models import Post
# from .serializers import PostListSerializer, PostCreateSerializer, PostDetailSerializer
# from .permissions import IsAuthor, IsAuthorOrAdmin
#
#
# class PostListCreateView(generics.ListCreateAPIView):
#     queryset = Post.objects.all()
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
#     serializer_class = PostListSerializer
#
#     def perform_create(self, serializer):
#         serializer.save(owner=self.request.user)
#
#     def get_serializer_class(self):
#         if self.request.method == 'GET':
#             return PostListSerializer
#         return PostCreateSerializer
#
#
# class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Post.objects.all()
#
#     def get_serializer_class(self):
#         if self.request.method in ('PUT', 'PATCH'):
#             return PostCreateSerializer
#         return PostDetailSerializer
#
#     def get_permissions(self):
#         if self.request.method == 'DELETE':
#             return IsAuthorOrAdmin(),
#         elif self.request.method in ('PUT', 'PATCH'):
#             return IsAuthor(),
#         return permissions.AllowAny(),
#
#

from rest_framework.viewsets import ModelViewSet
from .models import Post
from . import serializers
from rest_framework import permissions
from .permissions import IsAuthorOrAdmin
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend


class StandartPagination(PageNumberPagination):
    page_size = 2
    page_query_param = 'page'


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    pagination_class = StandartPagination
    filter_backends = (SearchFilter, )
    search_fields = ('title', )
    filterset_fields = ('category', 'created_at')

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.PostListSerializer
        elif self.action in ('create', 'update', 'partial_update'):
            return serializers.PostCreateSerializer
        return serializers.PostDetailSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        if self.action in ('update', 'partial_update', 'destroy'):
            return [permissions.IsAuthenticated(), IsAuthorOrAdmin()]
        return permissions.IsAuthenticatedOrReadOnly(),


