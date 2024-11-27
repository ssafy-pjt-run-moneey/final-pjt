from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.hashers import check_password
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserSerializer, UserProfileSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from products.models import Product
from products.serializers import ProductSerializer
from django.shortcuts import get_object_or_404
from articles.serializers import ArticleSerializer
from articles.models import Article
from rest_framework.views import APIView
from django.contrib.auth import update_session_auth_hash

User = get_user_model()

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
    email = request.data.get('email')
    password = request.data.get('password')
    user = authenticate(request, email=email, password=password)
    
    if user is not None:
        login(request, user)
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)
    else:
        return Response({'error': '이메일 또는 비밀번호가 잘못되었습니다.'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    try:
        refresh_token = request.data["refresh"]
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response(status=status.HTTP_205_RESET_CONTENT)
    except Exception as e:
        return Response(status=status.HTTP_400_BAD_REQUEST)

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

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_dog_type(request):
    user = request.user
    dog_type = request.data.get('dog_type')
    
    if dog_type is not None:
        try:
            dog_type = int(dog_type)
            if 1 <= dog_type <= 16:
                user.dog_type = dog_type
                user.save()
                return Response({
                    'status': 'success',
                    'message': 'Dog type updated successfully',
                    'dog_type': dog_type
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'status': 'error',
                    'message': 'Invalid dog type. Must be between 1 and 16.'
                }, status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            return Response({
                'status': 'error',
                'message': 'Invalid dog type. Must be an integer.'
            }, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({
            'status': 'error',
            'message': 'Dog type is required.'
        }, status=status.HTTP_400_BAD_REQUEST)
    


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request, user_id=None):
    if user_id:
        user = get_object_or_404(User, id=user_id)
    else:
        user = request.user

    data = {
        'id': user.id,
        'email': user.email,
        'username': user.username,
        'profile_img': request.build_absolute_uri(user.profile_img.url) if user.profile_img else None,
        'dog_type': user.dog_type,
        'created_date': user.created_date,
        'followers': UserProfileSerializer(user.followers.all(), many=True, context={'request': request}).data,
        'following': UserProfileSerializer(user.following.all(), many=True, context={'request': request}).data,
        'followers_count': user.followers.count(),
        'following_count': user.following.count(),
        'marked_products': ProductSerializer(
            Product.objects.filter(productmark__user=user),
            many=True
        ).data,
        'articles': ArticleSerializer(
            Article.objects.filter(user=user).order_by('-created_at'),
            many=True
        ).data,
    }
    return Response(data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    user = request.user
    serializer = UserProfileSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def toggle_follow(request, user_id):
    user_to_follow = get_object_or_404(User, id=user_id)
    
    # 자기 자신을 팔로우하는 것 방지
    if request.user.id == user_id:
        return Response({'error': '자기 자신을 팔로우할 수 없습니다.'}, status=400)

    # 현재 사용자의 following 목록에서 대상 사용자를 확인
    if request.user.following.filter(id=user_id).exists():
        # 언팔로우: 현재 사용자의 following에서 제거
        request.user.following.remove(user_to_follow)
        return Response({
            'status': 'unfollowed',
            'followers_count': user_to_follow.followers.count(),
            'following_count': user_to_follow.following.count()
        })
    
    # 팔로우: 현재 사용자의 following에 추가
    request.user.following.add(user_to_follow)
    return Response({
        'status': 'followed',
        'followers_count': user_to_follow.followers.count(),
        'following_count': user_to_follow.following.count()
    })

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_account(request):
    request.user.delete()
    return Response({'message': '계정이 삭제되었습니다.'})

class PasswordChangeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        old_password = request.data.get('old_password')
        new_password1 = request.data.get('new_password1')
        new_password2 = request.data.get('new_password2')

        if not user.check_password(old_password):
            return Response({'error': '현재 비밀번호가 일치하지 않습니다.'}, 
                          status=status.HTTP_400_BAD_REQUEST)

        if new_password1 != new_password2:
            return Response({'error': '새 비밀번호가 일치하지 않습니다.'}, 
                          status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password1)
        user.save()
        update_session_auth_hash(request, user)  # 세션 유지
        
        return Response({'message': '비밀번호가 성공적으로 변경되었습니다.'}, 
                      status=status.HTTP_200_OK)