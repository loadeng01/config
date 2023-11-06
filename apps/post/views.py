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
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .models import Post
from . import serializers
from rest_framework import permissions
from .permissions import IsAuthorOrAdmin
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from ..comment.models import Comment
from ..comment.serializers import CommentSerializer
from ..feedback.models import Like


class StandartPagination(PageNumberPagination):
    page_size = 3
    page_query_param = 'page'


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    pagination_class = StandartPagination
    filter_backends = (SearchFilter, DjangoFilterBackend)
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

    @action(['POST'], detail=True)
    def likes(self, request, pk, like_id=None):
        post = self.get_object()
        user = request.user
        like, is_created = Like.objects.get_or_create(post=post, owner=user)

        if is_created:
            return Response('Liked', status=200)
        like.is_liked = not like.is_liked
        like.save()

        if like.is_liked:
            return Response('Liked', status=200)
        return Response('Unliked', status=200)

    @action(['GET', 'POST', 'DELETE'], detail=True)
    def comments(self, request, pk, comment_id=None):
        if request.method == 'GET':
            post = self.get_object()
            comment = post.comments.all()
            serializer = CommentSerializer(
                instance=comment,
                many=True
            )
            return Response(serializer.data, status=200)

        elif request.method == 'POST':
            post = self.get_object()
            user = request.user
            body = request.data.get('body', 'message is empty')
            serializer = CommentSerializer(
                data={
                    'post': post.id,
                    'body': body
                }
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(owner=user)
            return Response(serializer.data, status=201)

        elif request.method == 'DELETE':
            comment_id = request.query_params.get('comment_id')
            if comment_id:
                comment = get_object_or_404(
                    Comment,
                    id=comment_id,
                    post__id=pk
                )
                comment.delete()
                return Response('Comment successfully deleted', status=204)
            return Response('Invalid comment_id', status=404)


