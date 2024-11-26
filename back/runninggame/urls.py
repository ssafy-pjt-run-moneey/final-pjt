from django.urls import path
from . import views

urlpatterns = [
    path('test/submit_test/', views.submit_test, name='submit_test'),
]