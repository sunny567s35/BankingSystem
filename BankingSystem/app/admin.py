from .models import Account, Transaction , Customer, Address
from django.contrib import admin
from .models import Transaction,Branch, Withdraw, Deposit, TransferIn, TransferOut, AccountType, Balance, Login, Logout
from django.contrib import admin


admin.site.register(Withdraw)
admin.site.register(Deposit)
admin.site.register(TransferIn)
admin.site.register(TransferOut)
admin.site.register(AccountType)
admin.site.register(Balance)
admin.site.register(Login)
admin.site.register(Logout)
admin.site.register(Branch)
# Register your models here.
admin.site.register(Account)
admin.site.register(Transaction)
admin.site.register(Customer)
admin.site.register(Address)
