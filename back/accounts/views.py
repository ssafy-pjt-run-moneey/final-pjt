from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.hashers import check_password
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def signup_view(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        # 기본 프로필 이미지와 one_type 설정
        user.profile_img = 'profiles/default.jpg'
        user.one_type = 0
        user.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    
    if user:
        refresh = RefreshToken.for_user(user)
        return Response({
            'key': str(refresh.access_token)  # Vue store에서 key로 받고 있으므로 변경
        })
    return Response({'error': '아이디 또는 비밀번호가 잘못되었습니다.'}, status=400)

@api_view(['POST'])
def logout_view(request):
    # 로그아웃 로직 (토큰 블랙리스트 등) 필요 시 구현
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    user = request.user
    old_password = request.data.get('old_password')
    new_password = request.data.get('new_password')
    
    if not check_password(old_password, user.password):
        return Response({'error': '현재 비밀번호가 일치하지 않습니다.'}, status=400)
    
    user.set_password(new_password)
    user.save()
    return Response({'message': '비밀번호가 성공적으로 변경되었습니다.'})