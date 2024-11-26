from django.db import models
from accounts.models import User
from django.conf import settings

class Article(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    content = models.TextField()
    image = models.ImageField(upload_to='articles/', blank=True, null=True)  # 이미지 필드
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    profile_img = models.ImageField(upload_to='profiles/', blank=True, null=True)  # 프로필 이미지 필드 추가
    username = models.CharField(max_length=50, blank=True, null=True)  # 사용자 이름 필드 추가