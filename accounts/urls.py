from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from .forms import CustomPasswordResetForm
urlpatterns = [
    path('', views.home, name="home"),
    path('register/', views.register, name="register"),
    path('activate_user/<uidb64>/<token>/', views.activate_user, name="activate_user"),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('not_email_verified/', views.not_email_verified, name="not_email_verified"),
    
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name="accounts/forget-password.html", 
        form_class=CustomPasswordResetForm), name="password_reset"),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('reset/done', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),

    path('terms_of_service', views.terms_of_service, name="terms_of_service"),
    path('user_profile', views.user_profile, name="user_profile"),
]