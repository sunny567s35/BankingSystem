import uuid
import random
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


def generate_account_number():
    return str(uuid.uuid4().int)[:12]  # Takes the first 12 digits of UUID


# 🔹 Deleted Account Model (New)
class DeletedAccount(models.Model):
    original_id = models.PositiveIntegerField()  # Original account ID
    customer_name = models.CharField(max_length=255)
    account_number = models.CharField(max_length=12)
    account_type = models.CharField(max_length=50)
    branch_name = models.CharField(max_length=255)
    balance_at_deletion = models.DecimalField(max_digits=15, decimal_places=2)
    closed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    deletion_date = models.DateTimeField(auto_now_add=True)
    reason = models.TextField(blank=True, null=True)
    customer_email = models.EmailField()  # For potential recovery
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    last_transaction_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Deleted Account"
        verbose_name_plural = "Deleted Accounts"
        ordering = ['-deletion_date']

    def __str__(self):
        return f"Deleted Account: {self.account_number} ({self.customer_name})"

# 🔹 Branch Model (Modified)
class Branch(models.Model):
    branch_name = models.CharField(max_length=255, unique=True)
    location = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    # Fix: Change related_name to avoid conflict
    accounts = models.ManyToManyField('Account', related_name='branch_accounts', blank=True)

    def __str__(self):
        return self.branch_name


# # 🔹 Employee Model
# class Employee(models.Model):
#     branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name="employees")
#     supervisor = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name="subordinates")
#     first_name = models.CharField(max_length=100)
#     last_name = models.CharField(max_length=100)
#     email = models.EmailField(unique=True)
#     phone = models.CharField(max_length=15, unique=True)
#     position = models.CharField(max_length=100)
#     salary = models.DecimalField(max_digits=15, decimal_places=2)
#     hire_date = models.DateField()
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.first_name} {self.last_name} ({self.position})"

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE ,null = True)
  #  employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, related_name="customers")
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True, null = True, blank = True)
    date_of_birth = models.DateField(null = True, blank = True)
    
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], null = True, blank = True)
    
    occupation = models.CharField(max_length=100, blank=True, null=True)
    income = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

# 🔹 Address Model
class Address(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="customer_address")
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

# 🔹 Account Type Model (Modified)
class AccountType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    min_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    # Fix: Change related_name to avoid conflict
    accounts = models.ManyToManyField('Account', related_name='account_type_accounts', blank=True)

    def __str__(self):
        return self.name

# 🔹 Account Model
class Account(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="accounts")
    account_type = models.ForeignKey(AccountType, on_delete=models.CASCADE, related_name="account_list")
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name="account_list")
    
    account_number = models.CharField(max_length=12, unique=True, editable=False, default=generate_account_number)
    password = models.CharField(max_length=128, default=make_password(''))  # Store hashed password
    
    last_transaction_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        """Ensure password is hashed before saving."""
        if self.password and not self.password.startswith("pbkdf2_sha256$"):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.account_number} - {self.customer.first_name} {self.customer.last_name}"
    
    def delete(self, *args, **kwargs):
        """Move account to DeletedAccount before deleting."""
        DeletedAccount.objects.create(
            original_id=self.id,
            customer_name=f"{self.customer.first_name} {self.customer.last_name}",
            account_number=self.account_number,
            account_type=self.account_type.name,
            branch_name=self.branch.branch_name,
            balance_at_deletion=self.balance.balance_amount if hasattr(self, 'balance') else 0,
            closed_by=kwargs.pop('deleted_by', None),
            reason=kwargs.pop('reason', None),
            customer_email=self.customer.email,
            phone_number=self.customer.phone,
            last_transaction_date=self.last_transaction_date
        )
        
        # Deactivate the associated user instead of deleting
        if hasattr(self.customer, 'user'):
            user = self.customer.user
            user.is_active = False
            user.username = f"deleted_{user.username}_{self.account_number[-4:]}"
            user.save()
        
        # Proceed with normal deletion
        super().delete(*args, **kwargs)

# 🔹 Transactions Model
class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('Deposit', 'Deposit'),
        ('Withdraw', 'Withdraw'),
        ('Transfer In', 'Transfer In'),
        ('Transfer Out', 'Transfer Out'),
        ('Interest', 'Interest')
    ]
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="transactions")
    transaction_type = models.CharField(max_length=15, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type} - {self.amount} - {self.account.account_number}"

# 🔹 Balance Model
class Balance(models.Model):
    account = models.OneToOneField(Account, on_delete=models.CASCADE, related_name="balance")
    balance_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    updated_at = models.DateTimeField(auto_now=True)

# 🔹 Announcements Model
class Announcements(models.Model):
    title = models.CharField(max_length=200, null=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Announcements"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

# 🔹 Interest Table Model
class InterestTable(models.Model):
    account_type = models.ForeignKey(AccountType, on_delete=models.CASCADE)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    last_updated = models.DateTimeField(auto_now=True)

class Withdraw(models.Model):
    transaction = models.OneToOneField(Transaction, on_delete=models.CASCADE)

# 🔹 Deposit Model
class Deposit(models.Model):
    transaction = models.OneToOneField(Transaction, on_delete=models.CASCADE)


# 🔹 TransferIn Model
class TransferOut(models.Model):
    from_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="transfers_out")
    to_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="incoming_transfers")
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    recipient_account_number = models.CharField(max_length=12)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transfer Out {self.amount} from {self.from_account.account_number} to {self.recipient_account_number} on {self.timestamp}"

class TransferIn(models.Model):
    from_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="outgoing_transfers")
    to_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="transfers_in")
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    sender_account_number = models.CharField(max_length=12)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transfer In {self.amount} to {self.to_account.account_number} from {self.sender_account_number} on {self.timestamp}"
    
    
# 🔹 Login Model
class Login(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    customer_name = models.CharField(max_length=255, null=True, blank=True)
    account_number = models.CharField(max_length=50, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    def __str__(self):
        name = self.customer_name or (self.customer.first_name + ' ' + self.customer.last_name) if self.customer else "Unknown"
        return f"{name} logged in on {self.timestamp}"

class Logout(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    customer_name = models.CharField(max_length=255, null=True, blank=True)
    account_number = models.CharField(max_length=50, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    def __str__(self):
        name = self.customer_name or (self.customer.first_name + ' ' + self.customer.last_name) if self.customer else "Unknown"
        return f"{name} logged out on {self.timestamp}"

# 🔹 Edit Account Model (Updated)
class EditAccount(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="modifications")
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, 
                                  limit_choices_to={'is_superuser': True},
                                  related_name="account_modifications")
    changes = models.JSONField(default=dict)  # Store all changes as JSON
    timestamp = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)  # Optional notes about the modification

    class Meta:
        ordering = ['-timestamp']
        verbose_name = "Account Modification"
        verbose_name_plural = "Account Modifications"

    def __str__(self):
        return f"{self.account.account_number} modified by {self.modified_by} at {self.timestamp}"

    def save(self, *args, **kwargs):
        """Ensure only superusers can be set as modified_by"""
        if self.modified_by and not self.modified_by.is_superuser:
            raise ValueError("Only superusers can be set as modifiers")
        super().save(*args, **kwargs)


# Add this to your models.py
class Ticket(models.Model):
    TICKET_TYPES = [
        ('account_change', 'Account Detail Change Request'),
        ('issue', 'Technical Issue'),
        ('general', 'General Inquiry'),
        ('security', 'Security Concern'),
    ]
    
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]
    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='tickets')
    ticket_type = models.CharField(max_length=20, choices=TICKET_TYPES)
    subject = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    admin_notes = models.TextField(blank=True, null=True)
    resolution = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Customer Ticket"
        verbose_name_plural = "Customer Tickets"
    
    def __str__(self):
        return f"Ticket #{self.id} - {self.get_ticket_type_display()} ({self.status})"