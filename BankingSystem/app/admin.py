from django.contrib import admin
from .models import (
    Account, Transaction, Customer, Address, Branch, Withdraw, Deposit, 
    TransferIn, TransferOut, AccountType, Balance, Login, Logout, 
    DeletedAccount, Announcements, InterestTable, EditAccount
)

admin.site.register(Withdraw)
admin.site.register(Deposit)
admin.site.register(TransferIn)
admin.site.register(TransferOut)
admin.site.register(AccountType)
admin.site.register(Balance)
admin.site.register(Login)
admin.site.register(Logout)
admin.site.register(Branch)
admin.site.register(Account)
admin.site.register(Transaction)
admin.site.register(Customer)
admin.site.register(Address)
admin.site.register(DeletedAccount)
admin.site.register(Announcements)
admin.site.register(InterestTable)

class EditAccountAdmin(admin.ModelAdmin):
    list_display = ('account', 'modified_by', 'timestamp', 'get_change_count', 'notes')
    list_filter = ('timestamp', 'modified_by')
    search_fields = ('account__account_number', 'modified_by__username')
    readonly_fields = ('timestamp',)
    
    def get_change_count(self, obj):
        return len(obj.changes) if obj.changes else 0
    get_change_count.short_description = 'Changes Count'
    
    def get_fields(self, request, obj=None):
        return ['account', 'modified_by', 'timestamp', 'changes', 'notes']
    
    def get_readonly_fields(self, request, obj=None):
        return ['timestamp'] + list(super().get_readonly_fields(request, obj))

admin.site.register(EditAccount, EditAccountAdmin)

from django.contrib import admin
from .models import Ticket

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'get_ticket_type_display', 'subject', 'get_status_display', 'created_at')
    list_filter = ('ticket_type', 'status', 'created_at')
    search_fields = ('subject', 'description', 'customer__first_name', 'customer__last_name')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('customer', 'ticket_type', 'subject', 'description', 'status')
        }),
        ('Admin Section', {
            'fields': ('admin_notes', 'resolution'),
            'classes': ('collapse',),
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if 'status' in form.changed_data and obj.status == 'resolved' and not obj.resolution:
            obj.resolution = "The issue has been resolved. Please contact us if you have any further questions."
        super().save_model(request, obj, form, change)