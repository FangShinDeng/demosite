from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name="home"),
    path('register/', views.register, name="register"),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('not_email_verified', views.not_email_verified, name="not_email_verified"),
    # path('register/done', view.register_done, name="register_done")
    # path('register/<uidb64>/<token>/, )
    path('password_reset/', auth_views.PasswordResetView.as_view(), name="password_reset"),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('reset/done', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
]