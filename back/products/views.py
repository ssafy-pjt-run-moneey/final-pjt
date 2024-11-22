# product/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django_filters import rest_framework as filters
from .models import Product, ProductMark, ProductComment
from .serializers import ProductSerializer, ProductCommentSerializer

class ProductFilter(filters.FilterSet):
    kor_co_nm = filters.CharFilter(lookup_expr='icontains')
    save_trm = filters.NumberFilter(method='filter_save_trm')

    class Meta:
        model = Product
        fields = ['kor_co_nm']

    def filter_save_trm(self, queryset, name, value):
        if value == 6:
            return queryset.filter(options__save_trm__lte=6)
        elif value == 12:
            return queryset.filter(options__save_trm__gt=6, options__save_trm__lte=12)
        elif value == 13:
            return queryset.filter(options__save_trm__gt=12)
        return queryset

class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filterset_class = ProductFilter
    permission_classes = [IsAuthenticatedOrReadOnly]

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def mark(self, request, pk=None):
        product = self.get_object()
        mark, created = ProductMark.objects.get_or_create(
            user=request.user,
            product=product
        )
        if not created:
            mark.delete()
            return Response({'status': 'unmarked'})
        return Response({'status': 'marked'})

    @action(detail=True, methods=['get', 'post'], permission_classes=[IsAuthenticatedOrReadOnly])
    def comments(self, request, pk=None):
        product = self.get_object()
        
        if request.method == 'GET':
            comments = ProductComment.objects.filter(product=product)
            serializer = ProductCommentSerializer(comments, many=True)
            return Response(serializer.data)
            
        elif request.method == 'POST':
            serializer = ProductCommentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user, product=product)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)