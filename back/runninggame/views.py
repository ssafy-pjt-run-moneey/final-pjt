from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json

@csrf_exempt
@require_POST
def submit_test(request):
    data = json.loads(request.body)
    # 여기에 테스트 결과를 처리하는 로직을 구현하세요
    return JsonResponse({'status': 'success'})