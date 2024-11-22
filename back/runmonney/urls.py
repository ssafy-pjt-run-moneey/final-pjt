# finance_project/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from accounts import views
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path('admin/', admin.site.urls),
    path('articles/', include('articles.urls')),
    path('accounts/signup/', include('dj_rest_auth.registration.urls')),
    path('accounts/', include('dj_rest_auth.urls')),
    path('api/v1/exchange/', include('exchange.urls')),
    path('api/runninggame/', include('runninggame.urls')),
    path('accounts/update_dog_type/', views.update_dog_type, name='update_dog_type'),
    # 금융 상품 관련 URL
    path('api/v1/financial/', include('products.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)