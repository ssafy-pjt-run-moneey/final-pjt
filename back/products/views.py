# products/views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
import requests
from django.conf import settings
from .models import Product, Option, ProductMark, ProductComment
from .serializers import ProductSerializer, ProductCommentSerializer

def fetch_products():
    url = "http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json"
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
            return False
            
        base_list = data.get('result', {}).get('baseList', [])  # result 키로 접근
        option_list = data.get('result', {}).get('optionList', [])
        
        for product_data in base_list:
            product, _ = Product.objects.update_or_create(
                fin_prdt_cd=product_data['fin_prdt_cd'],
                defaults={
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
                        'intr_rate': float(option_data.get('intr_rate', 0) or 0),  # None 처리
                        'intr_rate2': float(option_data.get('intr_rate2', 0) or 0),  # None 처리
                    }
                )
            except (Product.DoesNotExist, ValueError, TypeError) as e:
                print(f"Error processing option: {e}")
                continue
        
        return True
    except Exception as e:
        print(f"Error fetching products: {e}")
        return False

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
def product_detail(request, pk):
    try:
        product = Product.objects.prefetch_related('options').get(pk=pk)
        serializer = ProductSerializer(product, context={'request': request})
        return Response(serializer.data)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=404)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    mark, created = ProductMark.objects.get_or_create(
        user=request.user,
        product=product
    )
    if not created:
        mark.delete()
        return Response({'status': 'unmarked'})
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