# products/urls.py
from django.urls import path
from . import views

app_name = 'products'

# products/urls.py
urlpatterns = [
    path('products/', views.product_list, name='product-list'),
    path('products/<int:pk>/', views.product_detail, name='product-detail'),
    path('products/<int:pk>/mark/', views.mark_product, name='mark-product'),
    path('products/<int:pk>/comments/', views.product_comments, name='product-comments'),
    path('products/marked/', views.marked_products, name='marked-products'), 
]