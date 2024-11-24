from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'nickname', 'profile_img', 'dog_type', 'password1', 'password2')
        read_only_fields = ('dog_type', 'profile_img')
        extra_kwargs = {
            'password1': {'write_only': True},
            'password2': {'write_only': True}
        }

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("비밀번호가 일치하지 않습니다.")
        return data

    def create(self, validated_data):
        password = validated_data.pop('password1')
        validated_data.pop('password2')  # password2는 제거
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            nickname=validated_data.get('nickname', ''),
            password=password
        )
        return user
    
from rest_framework import serializers
from .models import User

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 
            'email', 
            'username', 
            'profile_img',
            'dog_type',
            'created_date',
            'updated_date'
        ]
        read_only_fields = ['email', 'created_date', 'updated_date']