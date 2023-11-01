from rest_framework import serializers
from .models import Post, PostImages
from ..category.models import Category


class PostListSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')

    class Meta:
        model = Post
        fields = ('id', 'title', 'owner', 'category_name', 'preview')


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


