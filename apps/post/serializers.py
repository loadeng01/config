from rest_framework import serializers
from .models import Post


class PostListSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')

    class Meta:
        model = Post
        fields = ('id', 'title', 'category', 'owner', 'preview', 'category_name')




