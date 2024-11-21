from django.urls import path
from . import views
from .views import exchange_rate_api

app_name = 'exchange'
urlpatterns = [
    # path('', views.exchange, name='exchange'),
    path('calculate/', views.exchange_rate_api, name='calculate'),
    path('exchange-rate/', exchange_rate_api, name='exchange_rate_api'),
]