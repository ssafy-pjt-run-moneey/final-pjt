from django.urls import path
from . import views

urlpatterns = [
    path('', views.article_list, name='article_list'),
    path('<int:article_pk>/', views.article_detail),
    path('comments/', views.comment_list),
    path('comments/<int:comment_pk>/', views.comment_detail),
    path('<int:article_pk>/comments/', views.comment_create),
    path('<int:article_pk>/update/', views.article_update),
    path('users/me/', views.get_user_info),
    path('comments/<int:comment_pk>/', views.comment_update_delete),
]