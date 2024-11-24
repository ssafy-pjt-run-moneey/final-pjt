from rest_framework import serializers
from .models import Article, Comment

class ArticlesListSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Article
        fields = '__all__'

from rest_framework import serializers
from .models import Comment

class CommentSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')  # 작성자 이름 추가

    class Meta:
        model = Comment
        fields = ['id', 'content', 'article', 'username', 'created_at', 'updated_at']
        read_only_fields = ['article', 'username', 'created_at', 'updated_at']

        
                      
class ArticleSerializer(serializers.ModelSerializer):
    # comment_set = CommentSerializer(many=True, read_only=True)
    # comment_count = serializers.IntegerField(source='comment_set.count', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    like_users = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    #like_users는 manytomany로 정의되있어서 이렇게 따로 직렬화 필드를 추가시켜주어야함

    class Meta:
        model = Article
        fields = '__all__'
        read_only_fields = ('user',)