# accounts/serializers.py
from rest_framework import serializers
from .models import User
from dj_rest_auth.registration.serializers import RegisterSerializer

class UserSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    is_following = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'nickname', 
            'profile_img', 'dog_type', 'password1', 'password2',
            'followers_count', 'following_count', 'is_following'
        )
        read_only_fields = ('dog_type', 'profile_img')
        extra_kwargs = {
            'password1': {'write_only': True},
            'password2': {'write_only': True}
        }

    def get_followers_count(self, obj):
        return obj.followers.count()

    def get_following_count(self, obj):
        return obj.following.count()
    
    def get_is_following(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return request.user.following.filter(id=obj.id).exists()
        return False

    # 기존 validate 메서드 유지
    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("비밀번호가 일치하지 않습니다.")
        return data

    # 기존 create 메서드 유지
    def create(self, validated_data):
        password = validated_data.pop('password1')
        validated_data.pop('password2')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            nickname=validated_data.get('nickname', ''),
            password=password
        )
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    is_following = serializers.SerializerMethodField()
    user_id = serializers.IntegerField(source='id', read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 
            'user_id',
            'email', 
            'username', 
            'profile_img',
            'dog_type',
            'created_date',
            'updated_date',
            'followers_count',
            'following_count',
            'is_following'
        ]
        read_only_fields = ['email', 'created_date', 'updated_date']

    def get_followers_count(self, obj):
        return obj.followers.count()

    def get_following_count(self, obj):
        return obj.following.count()

    def get_is_following(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return request.user.following.filter(id=obj.id).exists()
        return False

class CustomRegisterSerializer(RegisterSerializer):
    nickname = serializers.CharField(required=False, allow_blank=True, max_length=255)

    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username', ''),
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
            'nickname': self.validated_data.get('nickname', ''),
        }