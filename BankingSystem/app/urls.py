from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('send-otp/', views.send_otp, name='send_otp'),
    path('login/', views.login, name='login'),  # Ensure this line is present
    path('dashboard/<str:username>/', views.dashboard, name='dashboard'),
    path('user_logout/', views.user_logout, name='user_logout'),
    path('dashboard/<str:username>/deposit/', views.deposit, name='deposit'),
    path('validate_account/<str:account_number>/', views.validate_account, name='validate_account'),
    path('dashboard/<str:username>/statement/', views.statement, name='statement'),
    path('dashboard/<str:username>/withdraw/', views.withdraw, name='withdraw'),
    path('dashboard/<str:username>/transfer/', views.transfer, name='transfer'),
    path('download_statement_pdf/', views.download_statement_pdf, name='download_statement_pdf'),
    path('interest/', views.interest, name='interest'),
    path('dashboard/<str:username>/interest_summary/', views.interest_summary, name='interest_summary'),
    path('get_user/', views.get_user, name='get_user'),
    path('my_profile/<str:username>/', views.my_profile, name='my_profile'),
    path("verify_balance_password/", views.verify_balance_password, name="verify_balance_password"),
    path("password_reset/", views.password_reset, name="password_reset"),
    path("change_password/<str:username>/", views.change_password, name="change_password"),
    path("about/", views.about, name="about"),
    path('tickets/<path:username>/', views.view_tickets, name='view_tickets'),
    path('raise-ticket/<str:username>/', views.raise_ticket, name='raise_ticket'),
    path('user_ticket_detail/<str:username>/<int:ticket_id>/', views.user_ticket_detail, name='user_ticket_detail'),
    path('get-csrf-token/', views.get_csrf_token, name='get_csrf_token'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path("send_otp/", views.send_otp, name="send_otp"),
    path('verify_otp/', views.verify_otp, name='verify_otp'),

]