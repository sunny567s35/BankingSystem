"""
URL configuration for BankingSystem project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from app import views
from django.contrib.auth import views as auth_views
from django_prometheus.exports import ExportToDjangoView

urlpatterns = [
    path('', include('app.urls')),
    path('home/', views.home, name='home'),
    path("admin/", admin.site.urls),
    path('login/', views.login, name='login'),
    path('dashboard/<str:username>/', views.dashboard, name='dashboard'),
    path('password_reset/<str:username>/', views.password_reset, name='password_reset'),
    path('change_password/<str:username>/', views.change_password, name='change_password'),
    path('register/', views.register, name='register'),
    path('user_logout/', views.user_logout, name='user_logout'),
    path('dashboard/<str:username>/profile/', views.my_profile, name='profile'),
    path('dashboard/<str:username>/deposit/', views.deposit, name='deposit'),
    path('dashboard/<str:username>/withdraw/', views.withdraw, name='withdraw'),
    path('dashboard/<str:username>/transfer/', views.transfer, name='transfer'),
    path('dashboard/<str:username>/statement/', views.statement, name='statement'),
    path('download_statement/', views.download_statement_pdf, name='download_statement_pdf'),
    path('dashboard/<str:username>/interest/', views.interest, name='interest'),
    path('validate_account/<str:account_number>/', views.validate_account, name='validate_account'),
    path('interest/', views.interest, name='interest'),
    path('dashboard/<str:username>/interest_summary/', views.interest_summary, name='interest_summary'),
    path('dashboard/<str:username>/statement/', views.statement, name='statement'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='accounts_login'),  # Add this
    path("verify-balance-password/", views.verify_balance_password, name="verify_balance_password"),
    path('download_statement_pdf/', views.download_statement_pdf, name='download_statement_pdf'),
    path('about/', views.about, name='about'),
    path('setting/<str:username>/', views.setting, name='setting'),
    path('custom_admin/', include('Custom_admin.urls')),
    path('send-otp/', views.send_otp, name='send_otp'),
    path('get_user/', views.get_user, name='get_user'),
    path('my_profile/<str:username>/', views.my_profile, name='my_profile'),
    path('verify-balance-password/', views.verify_balance_password, name='verify_balance_password'),
    path('tickets/<path:username>/', views.view_tickets, name='view_tickets'),
    path('raise-ticket/<str:username>/', views.raise_ticket, name='raise_ticket'),
    path('get-csrf-token/', views.get_csrf_token, name='get_csrf_token'),
    path('user_ticket_detail/<str:username>/<int:ticket_id>/', views.user_ticket_detail, name='user_ticket_detail'),
    path("metrics/", ExportToDjangoView, name="metrics"),
]
