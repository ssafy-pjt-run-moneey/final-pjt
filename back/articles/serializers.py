from rest_framework import serializers
from .models import Article, Comment

class ArticlesListSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    profile_img = serializers.ImageField(source='user.profile_img', read_only=True)  # 프로필 이미지 추가

    class Meta:
        model = Article
        fields = ['id', 'title', 'username', 'profile_img', 'created_at']

class CommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    profile_img = serializers.ImageField(source='user.profile_img', read_only=True)  # 프로필 이미지 추가

    class Meta:
        model = Comment
        fields = ['id', 'content', 'article', 'username', 'profile_img', 'created_at', 'updated_at']
        read_only_fields = ['article', 'username', 'profile_img', 'created_at', 'updated_at']

class ArticleSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    profile_img = serializers.ImageField(source='user.profile_img', read_only=True)  # 프로필 이미지 추가

    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'username', 'profile_img', 'created_at']