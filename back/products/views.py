# products/views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
import requests
from django.conf import settings
from .models import Product, Option, ProductMark, ProductComment
from .serializers import ProductSerializer, ProductCommentSerializer
from django.core.mail import send_mass_mail

def fetch_products():
    base_url = "http://finlife.fss.or.kr/finlifeapi/"
    product_types = {
        'deposit': 'depositProductsSearch.json',
        'savings': 'savingProductsSearch.json'
    }
    
    for product_type, endpoint in product_types.items():
        url = base_url + endpoint
        params = {
            'auth': settings.FSS_API_KEY,
            'topFinGrpNo': '020000',
            'pageNo': '1',
            'resultType': 'json'
        }
        
        try:
            response = requests.get(url, params=params)
            data = response.json()
            
            if response.status_code != 200:
                continue
                
            base_list = data.get('result', {}).get('baseList', [])
            option_list = data.get('result', {}).get('optionList', [])
            
            for product_data in base_list:
                product, _ = Product.objects.update_or_create(
                    fin_prdt_cd=product_data['fin_prdt_cd'],  # 이미 primary key로 사용되므로 그대로 유지
                    defaults={
                        'product_type': product_type,
                        'dcls_month': product_data.get('dcls_month', ''),
                        'fin_prdt_nm': product_data.get('fin_prdt_nm', ''),
                        'kor_co_nm': product_data.get('kor_co_nm', ''),
                        'etc_note': product_data.get('etc_note', ''),
                        'join_deny': int(product_data.get('join_deny', 0)),
                        'join_member': product_data.get('join_member', ''),
                        'join_way': product_data.get('join_way', ''),
                        'spcl_cnd': product_data.get('spcl_cnd', ''),
                    }
                )
            
            for option_data in option_list:
                try:
                    product = Product.objects.get(fin_prdt_cd=option_data['fin_prdt_cd'])
                    Option.objects.update_or_create(
                        product=product,
                        save_trm=option_data.get('save_trm', 0),
                        defaults={
                            'dcls_month': option_data.get('dcls_month', ''),
                            'intr_rate_type_nm': option_data.get('intr_rate_type_nm', ''),
                            'intr_rate': float(option_data.get('intr_rate', 0) or 0),
                            'intr_rate2': float(option_data.get('intr_rate2', 0) or 0),
                        }
                    )
                except (Product.DoesNotExist, ValueError, TypeError) as e:
                    print(f"Error processing option: {e}")
                    continue
                    
        except Exception as e:
            print(f"Error fetching {product_type} products: {e}")
            continue
    
    return True

@api_view(['GET'])
@permission_classes([AllowAny])
def product_list(request):
    try:
        success = fetch_products()
        if not success:
            return Response({"error": "Failed to fetch products from API"}, status=500)
        
        products = Product.objects.prefetch_related('options').all()
        serializer = ProductSerializer(products, many=True, context={'request': request})
        return Response(serializer.data)
    except Exception as e:
        print(f"Error in product_list: {e}")  # 서버 로그에 에러 출력
        return Response(
            {"error": "Internal server error occurred"}, 
            status=500
        )

@api_view(['GET'])
@permission_classes([AllowAny])
def product_detail(request, fin_prdt_cd):
    try:
        product = Product.objects.prefetch_related('options').get(fin_prdt_cd=fin_prdt_cd)
        serializer = ProductSerializer(product, context={'request': request})
        return Response(serializer.data)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=404)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_product(request, fin_prdt_cd):
    product = get_object_or_404(Product, fin_prdt_cd=fin_prdt_cd)
    mark, created = ProductMark.objects.get_or_create(
        user=request.user,
        product=product
    )
    if not created:
        mark.delete()
        product.subscribers.remove(request.user)  # 마킹 취소 시 구독도 취소
        return Response({'status': 'unmarked'})
    else:
        product.subscribers.add(request.user)  # 마킹 시 자동으로 구독 추가
    return Response({'status': 'marked'})

@api_view(['GET', 'POST'])
def product_comments(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'GET':
        comments = ProductComment.objects.filter(product=product).select_related('user')
        serializer = ProductCommentSerializer(comments, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        if not request.user.is_authenticated:
            return Response(status=401)
        serializer = ProductCommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, product=product)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def marked_products(request):
    marked = ProductMark.objects.filter(user=request.user).select_related('product')
    products = [mark.product for mark in marked]
    serializer = ProductSerializer(products, many=True, context={'request': request})
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])  # 관리자만 접근 가능하도록 수정 필요
def update_product_rates(request, fin_prdt_cd):
    try:
        product = Product.objects.get(fin_prdt_cd=fin_prdt_cd)
        options_data = request.data.get('options', [])
        
        # 금리 정보 업데이트
        for option_data in options_data:
            option = Option.objects.get(
                product=product,
                save_trm=option_data['save_trm']
            )
            option.intr_rate = option_data['intr_rate']
            option.intr_rate2 = option_data['intr_rate2']
            option.save()
        
        # 구독자들에게 이메일 발송
        subscribers = product.subscribers.all()
        if subscribers:
            emails = []
            for subscriber in subscribers:
                message = (
                    f'금리 정보 업데이트 알림',  # 제목
                    f'''안녕하세요, {subscriber.username}님.
                    
                    구독하신 상품 [{product.fin_prdt_nm}]의 금리가 변경되었습니다.
                    자세한 내용은 웹사이트에서 확인해주세요.
                    ''',  # 내용
                    settings.DEFAULT_FROM_EMAIL,  # 발신자
                    [subscriber.email],  # 수신자
                )
                emails.append(message)
            
            # 대량 이메일 발송
            send_mass_mail(emails, fail_silently=False)
        
        return Response({'message': '금리 정보가 업데이트되었습니다.'})
        
    except Product.DoesNotExist:
        return Response({'error': '상품을 찾을 수 없습니다.'}, status=404)
    except Exception as e:
        return Response({'error': str(e)}, status=400)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def subscribe_product(request, fin_prdt_cd):
    try:
        product = Product.objects.get(fin_prdt_cd=fin_prdt_cd)
        product.subscribers.add(request.user)
        return Response({'status': 'subscribed'})
    except Product.DoesNotExist:
        return Response({'error': '상품을 찾을 수 없습니다.'}, status=404)