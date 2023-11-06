from rest_framework import serializers
from .models import Post, PostImages
from ..category.models import Category
from apps.feedback.serializers import LikeSerializer
from apps.comment.serializers import CommentSerializer


class PostListSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')

    class Meta:
        model = Post
        fields = ('id', 'title', 'owner', 'category_name', 'preview')

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        likes = instance.likes.filter(is_liked=True)
        comments = instance.comments.all()
        serializer = CommentSerializer(comments, many=True)

        repr['likes count'] = len(likes)
        if comments:
            repr['comments'] = serializer.data
        return repr


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImages
        fields = '__all__'


class PostCreateSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(required=True, queryset=Category.objects.all())
    images = PostImageSerializer(many=True, required=False)

    class Meta:
        model = Post
        fields = ('title', 'body', 'category', 'preview', 'images')

    def create(self, validated_data):
        request = self.context.get('request')
        post = Post.objects.create(**validated_data)
        images_data = request.FILES.getlist('images')
        for image in images_data:
            PostImages.objects.create(image=image, post=post)
        return post


class PostDetailSerializer(serializers.ModelSerializer):
    owner_username = serializers.ReadOnlyField(source='owner.username')
    category_name = serializers.ReadOnlyField(source='category.name')
    images = PostImageSerializer(many=True)

    class Meta:
        model = Post
        fields = '__all__'

