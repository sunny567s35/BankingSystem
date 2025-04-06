from django.urls import path
from .views import (
    custom_admin_login, custom_admin_logout, custom_admin_dashboard, 
    new_account, manage_account, edit_account, delete_account, transactions_view, 
    deposit_view, withdraw_view, transfer_view, 
    admin_tickets_list, admin_pending_tickets, admin_resolved_tickets, admin_ticket_detail,
    announcements_view, create_announcement, delete_announcement
)



urlpatterns = [
    path('login/', custom_admin_login, name='custom_admin_login'),
    path("dashboard/", custom_admin_dashboard, name="custom_admin_dashboard"),
    path('new_account/', new_account, name='new_account'),
    path('manage-account/', manage_account, name='manage_account'),
    path('edit-account/<int:account_id>/', edit_account, name='edit_account'),
    path('delete-account/<int:account_id>/', delete_account, name='delete_account'),
    path('transactions/', transactions_view, name='transactions'),
    path('deposit/', deposit_view, name='deposit_view'),
    path('withdraw/', withdraw_view, name='withdraw_view'),
    path('transfer/', transfer_view, name='transfer_view'),
    path("logout/", custom_admin_logout, name="custom_admin_logout"),
    path('announcements/', announcements_view, name='announcements'),
    path('announcements/create/', create_announcement, name='create_announcement'),
    path('announcements/delete/<int:id>/', delete_announcement, name='delete_announcement'),
    path('tickets/', admin_tickets_list, name='admin_tickets_list'),
    path('tickets/pending/', admin_pending_tickets, name='admin_pending_tickets'),
    path('tickets/resolved/', admin_resolved_tickets, name='admin_resolved_tickets'),
    path('tickets/<int:ticket_id>/', admin_ticket_detail, name='admin_ticket_detail'),
]