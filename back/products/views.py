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
from django.contrib.auth import get_user_model

User = get_user_model()

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
@permission_classes([IsAuthenticated])
def product_comments(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'GET':
        comments = ProductComment.objects.filter(product=product).select_related('user')
        serializer = ProductCommentSerializer(comments, many=True)
        return Response(serializer.data)
        
    elif request.method == 'POST':
        serializer = ProductCommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, product=product)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def comment_detail(request, product_pk, comment_pk):
    comment = get_object_or_404(ProductComment, pk=comment_pk, product__fin_prdt_cd=product_pk)
    
    if comment.user != request.user:
        return Response({'error': '권한이 없습니다.'}, status=403)
    
    if request.method == 'PUT':
        serializer = ProductCommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
        
    elif request.method == 'DELETE':
        comment.delete()
        return Response(status=204)
    
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
    

# products/views.py

from django.db.models import Q
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Product, Option
from .serializers import ProductSerializer

from django.db.models import Q, Count
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Product, Option, ProductMark
from .serializers import ProductSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def recommendations(request):
    user_type = request.user.dog_type  # 사용자의 dog_type 가져오기
    personalized_products = []
    popular_products = []

    # 기본 쿼리셋 가져오기
    products = Product.objects.prefetch_related('options')

    # 각 dog_type에 따른 조건 설정 (조건 완화)
    if user_type == 1:  # 비숑 (XXXX)
        personalized_products = products.filter(
            options__save_trm__lte=12,  # 12개월 이하 단기 상품으로 확장
            product_type='deposit'
        ).distinct()[:4]

    elif user_type == 2:  # 푸들 (XXXO)
        personalized_products = products.filter(
            product_type='savings'  # 금리 조건 제거
        ).distinct()[:4]

    elif user_type == 3:  # 치와와 (XXOX)
        personalized_products = products.filter(
            product_type='deposit',
            options__save_trm__lte=6  # 기간을 6개월 이하로 완화
        ).distinct()[:4]

    elif user_type == 4:  # 슈나우저 (XXOO)
        personalized_products = products.filter(
            product_type='savings',
            options__save_trm__lte=24  # 기간을 최대 2년으로 확장
        ).distinct()[:4]

    elif user_type in [5, 7, 8, 13, 15]:  # 사모예드, 코커스파니엘, 보더콜리 등
        filtered_products = []
        for product in products.filter(product_type='savings'):
            for option in product.options.all():
                if option.save_trm >= 12:  # 최소 기간 조건만 유지
                    filtered_products.append(product)
                    break
        personalized_products = filtered_products[:4]

    elif user_type in [6, 9, 11, 12]:  # 바셋하운드, 포메라니안 등
        filtered_products = []
        for product in products.filter(product_type='deposit'):
            for option in product.options.all():
                if option.save_trm >= 6:  # 최소 기간 조건만 유지
                    filtered_products.append(product)
                    break
        personalized_products = filtered_products[:4]

    elif user_type in [10, 14]:  # 파피용, 시츄 등
        personalized_products = products.filter(
            product_type='savings'
        ).distinct()[:4]

    elif user_type == 16:  # 저먼셰퍼드 (OOOO)
        personalized_products = products.filter(
            product_type='deposit'
        ).distinct()[:4]

    # 추천 상품이 없을 경우 기본 상품 제공
    if not personalized_products:
        fallback_product = products.filter(product_type='deposit').first()
        if fallback_product:
            personalized_products = [fallback_product]

    # 비슷한 사람들이 많이 마킹한 상품 찾기
    similar_users = request.user.__class__.objects.filter(dog_type=user_type)  
    popular_product_ids = (
        ProductMark.objects.filter(user__in=similar_users)
        .values('product')
        .annotate(mark_count=Count('product'))
        .order_by('-mark_count')[:4]
        .values_list('product', flat=True)
    )
    popular_products = Product.objects.filter(fin_prdt_cd__in=popular_product_ids)

    # 직렬화 및 응답 반환
    serializer_personalized = ProductSerializer(personalized_products, many=True, context={'request': request})
    serializer_popular = ProductSerializer(popular_products, many=True, context={'request': request})

    return Response({
        'personalized': serializer_personalized.data,
        'popular': serializer_popular.data,
    })