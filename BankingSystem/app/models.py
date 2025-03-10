from django.db import models

from django.db import models

class Account(models.Model):
    ACCOUNT_TYPES = (
        ('savings', 'Savings'),
        ('current', 'Current'),
    )
    
    account_number = models.CharField(auto_created=True, max_length=50, unique=True)
    #pin = models.TextField()
    firstname = models.CharField(max_length=250)
    lastname = models.CharField(max_length=250)
    #middlename = models.CharField(max_length=250, blank=True, null=True)
    email = models.EmailField(unique = True)
    password = models.TextField()
    balance = models.FloatField(default=0.0)
    account_type = models.CharField(max_length=10, choices=ACCOUNT_TYPES)
    interest_rate = models.FloatField(default=0.03)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.account_number} - {self.firstname} {self.lastname}"

class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('deposit', 'Deposit'),
        ('withdrawal', 'Withdrawal'),
        ('transfer', 'Transfer'),
        ('interest_credit', 'Interest Credit'),
    )
    
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=15, choices=TRANSACTION_TYPES)
    amount = models.FloatField()
    balance_after = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type} - {self.amount} - {self.account.account_number}"
# Create your models here.
