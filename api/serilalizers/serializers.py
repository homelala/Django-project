import django_filters
from rest_framework import serializers

from api.model.models import Post, Comment, Category


class PostSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source="category.name", default="No Category")

    class Meta:
        model = Post
        fields = '__all__'


class CommentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["content", "created_at"]


class PostDetailSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source="category.name", default="No Category")
    tags = serializers.SlugRelatedField(many=True, slug_field="name", read_only=True)
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = Post
        fields = "__all__"


class PostPrevNextSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["title"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class PostFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    category = django_filters.CharFilter(field_name="category__name", lookup_expr='icontains')

    class Meta:
        model = Post
        fields = ["title", "category"]
