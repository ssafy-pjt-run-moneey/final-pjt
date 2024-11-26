from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
import json
from accounts.models import User  # CustomUser 모델을 import
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_test(request):
    data = request.data
    result_type = data.get('result_type')
    
    if result_type is not None:
        user = request.user
        user.update_dog_type(result_type)
        
        return JsonResponse({'status': 'success', 'message': 'Dog type updated successfully'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid result type'}, status=400)
    
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_dog_type(request):
    user = request.user
    dog_type = request.data.get('dog_type')
    
    if dog_type is not None:
        try:
            dog_type = int(dog_type)
            if 1 <= dog_type <= 16:
                user.update_dog_type(dog_type)
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