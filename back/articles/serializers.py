from rest_framework import serializers
from .models import Article, Comment

class ArticlesListSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    profile_img = serializers.ImageField(source='user.profile_img', read_only=True)
    user_id = serializers.IntegerField(source='user.id', read_only=True)

    class Meta:
        model = Article
        fields = ['id', 'title', 'username', 'profile_img', 'user_id', 'created_at']

class CommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    profile_img = serializers.ImageField(source='user.profile_img', read_only=True)
    user_id = serializers.IntegerField(source='user.id', read_only=True)  # 추가

    class Meta:
        model = Comment
        fields = ['id', 'content', 'article', 'username', 'profile_img', 'user_id', 'created_at', 'updated_at']  # user_id 추가
        read_only_fields = ['article', 'username', 'profile_img', 'user_id', 'created_at', 'updated_at']

class ArticleSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    profile_img = serializers.ImageField(source='user.profile_img', read_only=True)
    user_id = serializers.IntegerField(source='user.id', read_only=True)  # 추가
    image = serializers.ImageField(use_url=True, required=False)

    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'image', 'username', 'profile_img', 'user_id', 'created_at']  # user_id 추가
        read_only_fields = ['user', 'created_at']