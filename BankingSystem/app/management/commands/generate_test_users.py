import random
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import transaction
from faker import Faker
from app.models import *

fake = Faker()

class Command(BaseCommand):
    help = 'Generates 100 random users with bank accounts and transactions'

    def handle(self, *args, **options):
        # Create or get default account types
        savings_type, _ = AccountType.objects.get_or_create(
            name='Savings',
            defaults={'min_balance': 500.00, 'interest_rate': 0.50}
        )
        
        current_type, _ = AccountType.objects.get_or_create(
            name='Current',
            defaults={'min_balance': 1000.00, 'interest_rate': 0.25}
        )
        
        # Create or get default branches
        main_branch, _ = Branch.objects.get_or_create(
            branch_name='Main Branch',
            defaults={'location': '123 Main Street, City Center'}
        )
        
        north_branch, _ = Branch.objects.get_or_create(
            branch_name='North Branch',
            defaults={'location': '456 North Avenue, Suburb'}
        )
        
        south_branch, _ = Branch.objects.get_or_create(
            branch_name='South Branch',
            defaults={'location': '789 South Road, Downtown'}
        )
        
        branches = [main_branch, north_branch, south_branch]
        account_types = [savings_type, current_type]
        
        User = get_user_model()
        
        with transaction.atomic():
            for i in range(1, 101):
                try:
                    # Create user
                    first_name = fake.first_name()
                    last_name = fake.last_name()
                    email = f"{first_name.lower()}.{last_name.lower()}{i}@example.com"
                    
                    user = User.objects.create_user(
                        username=email,
                        email=email,
                        password='Test@123',
                        first_name=first_name,
                        last_name=last_name
                    )
                    
                    # Create customer - FIXED: Added missing closing parenthesis
                    customer = Customer.objects.create(
                        user=user,
                        first_name=first_name,
                        last_name=last_name,
                        email=email,
                        phone=fake.phone_number()[:15],
                        date_of_birth=fake.date_of_birth(minimum_age=18, maximum_age=80),
                        gender=random.choice(['Male', 'Female', 'Other']),
                        occupation=fake.job(),
                        income=random.randint(20000, 200000)
                    )  # This was missing in original code
                    
                    # Create address
                    Address.objects.create(
                        customer=customer,
                        street=fake.street_address(),
                        city=fake.city(),
                        state=fake.state(),
                        zip_code=fake.postcode(),
                        country=fake.country()
                    )
                    
                    # Select random account type and branch
                    account_type = random.choice(account_types)
                    branch = random.choice(branches)
                    
                    # Create account
                    account = Account.objects.create(
                        customer=customer,
                        account_type=account_type,
                        branch=branch,
                        password='pbkdf2_sha256$260000$...',  # This would be hashed in real scenario
                        last_transaction_date=fake.date_time_this_year()
                    )
                    
                    # Add account to branch and account type
                    branch.accounts.add(account)
                    account_type.accounts.add(account)
                    
                    # Create initial balance (between 1000 and 50000)
                    initial_balance = random.randint(1000, 50000)
                    balance = Balance.objects.create(
                        account=account,
                        balance_amount=initial_balance
                    )
                    
                    # Create initial deposit transaction
                    deposit_txn = Transaction.objects.create(
                        account=account,
                        transaction_type='Deposit',
                        amount=initial_balance,
                        timestamp=account.created_at - timedelta(minutes=5)
                    )
                    Deposit.objects.create(transaction=deposit_txn)
                    
                    # Generate random transactions (3-10 per account)
                    num_transactions = random.randint(3, 10)
                    for _ in range(num_transactions):
                        transaction_date = fake.date_time_between(
                            start_date=account.created_at,
                            end_date='now'
                        )
                        
                        # Randomly choose transaction type (weighted towards deposits)
                        txn_type = random.choices(
                            ['Deposit', 'Withdraw', 'Transfer Out'],
                            weights=[0.5, 0.3, 0.2],
                            k=1
                        )[0]
                        
                        amount = random.randint(100, 10000)
                        
                        if txn_type == 'Deposit':
                            balance.balance_amount += amount
                            txn = Transaction.objects.create(
                                account=account,
                                transaction_type=txn_type,
                                amount=amount,
                                timestamp=transaction_date
                            )
                            Deposit.objects.create(transaction=txn)
                        
                        elif txn_type == 'Withdraw':
                            if balance.balance_amount >= amount:
                                balance.balance_amount -= amount
                                txn = Transaction.objects.create(
                                    account=account,
                                    transaction_type=txn_type,
                                    amount=amount,
                                    timestamp=transaction_date
                                )
                                Withdraw.objects.create(transaction=txn)
                        
                        elif txn_type == 'Transfer Out':
                            if balance.balance_amount >= amount:
                                # Find a random recipient account (excluding current account)
                                recipient_accounts = Account.objects.exclude(id=account.id)
                                if recipient_accounts.exists():
                                    recipient = random.choice(recipient_accounts)
                                    recipient_balance = Balance.objects.get(account=recipient)
                                    
                                    # Update balances
                                    balance.balance_amount -= amount
                                    recipient_balance.balance_amount += amount
                                    recipient_balance.save()
                                    
                                    # Create transactions
                                    sender_txn = Transaction.objects.create(
                                        account=account,
                                        transaction_type='Transfer Out',
                                        amount=amount,
                                        timestamp=transaction_date
                                    )
                                    recipient_txn = Transaction.objects.create(
                                        account=recipient,
                                        transaction_type='Transfer In',
                                        amount=amount,
                                        timestamp=transaction_date
                                    )
                                    
                                    # Create transfer records
                                    TransferOut.objects.create(
                                        from_account=account,
                                        to_account=recipient,
                                        amount=amount,
                                        recipient_account_number=recipient.account_number,
                                        timestamp=transaction_date
                                    )
                                    TransferIn.objects.create(
                                        from_account=account,
                                        to_account=recipient,
                                        amount=amount,
                                        sender_account_number=account.account_number,
                                        timestamp=transaction_date
                                    )
                        
                        balance.save()
                        account.last_transaction_date = transaction_date
                        account.save()
                    
                    # Create login/logout records (2-5 sessions)
                    num_sessions = random.randint(2, 5)
                    for _ in range(num_sessions):
                        login_time = fake.date_time_this_year()
                        logout_time = login_time + timedelta(minutes=random.randint(5, 120))
                        
                        Login.objects.create(
                            customer=customer,
                            customer_name=f"{first_name} {last_name}",
                            account_number=account.account_number,
                            timestamp=login_time,
                            ip_address=fake.ipv4()
                        )
                        
                        Logout.objects.create(
                            customer=customer,
                            customer_name=f"{first_name} {last_name}",
                            account_number=account.account_number,
                            timestamp=logout_time,
                            ip_address=fake.ipv4()
                        )
                    
                    self.stdout.write(self.style.SUCCESS(f'Created user {i}: {email}'))
                
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error creating user {i}: {str(e)}'))
                    continue
        
        self.stdout.write(self.style.SUCCESS('Successfully created 100 test users with accounts and transactions!'))