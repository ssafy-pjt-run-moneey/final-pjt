from django.urls import path
from . import views

urlpatterns = [
    path('get/', views.exchange, name='get_exchange_rates'),
    path('convert/', views.convert_currency, name='convert_currency'),
]