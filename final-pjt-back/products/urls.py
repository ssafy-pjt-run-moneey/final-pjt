from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('products/marked/', views.marked_products, name='marked-products'),  # 이 패턴을 맨 위로
    path('products/', views.product_list, name='product-list'),
    path('products/<str:fin_prdt_cd>/mark/', views.mark_product, name='mark-product'),
    path('products/<str:fin_prdt_cd>/rates/', views.update_product_rates, name='update-rates'),
    path('products/<str:fin_prdt_cd>/', views.product_detail, name='product-detail'),
    path('products/<str:pk>/comments/', views.product_comments, name='product-comments'),
    path('products/<str:product_pk>/comments/<int:comment_pk>/', views.comment_detail, name='comment-detail'),
    path('recommendations/', views.recommendations, name='recommendations'),
]