from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        # 기본 프로필 이미지 설정
        user.profile_img = 'profiles/0.png'
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=20)
    profile_img = models.ImageField(upload_to='profiles/', default='profiles/0.png')
    dog_type = models.IntegerField(default=0)
    password1 = models.CharField(max_length=128)
    password2 = models.CharField(max_length=128)  # 비밀번호 확인용
    created_date = models.DateTimeField(auto_now_add=True)  # ERD의 created_date 필드
    updated_date = models.DateTimeField(auto_now=True)  # ERD의 updated_date 필드

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def update_dog_type(self, test_result):
        """테스트 결과에 따라 one_type 업데이트"""
        if 1 <= test_result <= 16:  # 유효한 테스트 결과 범위 확인
            self.dog_type = test_result
            # dog_type이 변경되면 프로필 이미지도 자동으로 업데이트
            self.profile_img = f'profiles/{test_result}.png'
            self.save()