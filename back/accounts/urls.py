from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('accounts/signup/', views.signup_view, name='signup'),
    path('accounts/login/', views.login_view, name='login'),
    path('accounts/logout/', views.logout_view, name='logout'),
    path('update_dog_type/', views.update_dog_type, name='update_dog_type'),
    path('profile/', views.user_profile, name='user-profile'),
    path('profile/<int:user_id>/', views.user_profile, name='user-profile-detail'),
    path('profile/update/', views.update_profile, name='update-profile'),
    path('profile/delete/', views.delete_account, name='delete-account'),
    path('follow/<int:user_id>/', views.toggle_follow, name='toggle-follow'),
    path('password/change/', views.PasswordChangeView.as_view(), name='password_change'),
]