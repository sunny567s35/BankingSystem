import random
from datetime import datetime, timedelta
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import transaction
from faker import Faker
from app.models import *

fake = Faker()

class Command(BaseCommand):
    help = 'Generates detailed transaction history for specific customers'

    def add_arguments(self, parser):
        parser.add_argument('--customer-id', type=int, help='Specific customer ID to generate transactions for')
        parser.add_argument('--num-transactions', type=int, default=50, help='Number of transactions to generate')

    def handle(self, *args, **options):
        customer_id = options['customer_id']
        num_transactions = options['num_transactions']
        
        try:
            customer = Customer.objects.get(id=customer_id)
            account = Account.objects.get(customer=customer)
            balance = Balance.objects.get(account=account)
            
            # Get all other accounts for transfers (excluding the customer's own account)
            other_accounts = Account.objects.exclude(id=account.id)
            
            if not other_accounts.exists():
                self.stdout.write(self.style.ERROR('Need at least one other account for transfers'))
                return
            
            with transaction.atomic():
                self.generate_transactions(account, balance, other_accounts, num_transactions)
                
            self.stdout.write(self.style.SUCCESS(
                f'Successfully generated {num_transactions} transactions for customer {customer_id}'
            ))
            
        except Customer.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Customer with ID {customer_id} not found'))
        except Account.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'No account found for customer {customer_id}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {str(e)}'))

    def generate_transactions(self, account, balance, other_accounts, num_transactions):
        start_date = datetime.now() - timedelta(days=365)  # 1 year history
        
        for i in range(num_transactions):
            # Random date within the last year (more recent transactions more likely)
            transaction_date = fake.date_time_between(
                start_date=start_date,
                end_date='now'
            )
            
            # Transaction type distribution
            txn_type = random.choices(
                ['Deposit', 'Withdraw', 'Transfer Out'],
                weights=[0.4, 0.3, 0.3],  # 40% deposits, 30% withdrawals, 30% transfers
                k=1
            )[0]
            
            # Generate reasonable amounts based on current balance
            if balance.balance_amount < Decimal('1000'):
                amount = Decimal(random.randint(100, 500))
            else:
                max_amount = min(Decimal('10000'), balance.balance_amount * Decimal('0.3'))
                amount = Decimal(random.randint(100, int(max_amount)))
            
            if txn_type == 'Deposit':
                self.create_deposit(account, balance, amount, transaction_date)
                
            elif txn_type == 'Withdraw':
                if balance.balance_amount >= amount:
                    self.create_withdrawal(account, balance, amount, transaction_date)
                else:
                    # If insufficient funds, make it a deposit instead
                    self.create_deposit(account, balance, amount, transaction_date)
                    
            elif txn_type == 'Transfer Out':
                if balance.balance_amount >= amount:
                    recipient = random.choice(other_accounts)
                    self.create_transfer(account, recipient, balance, amount, transaction_date)
                else:
                    # If insufficient funds, make it a deposit instead
                    self.create_deposit(account, balance, amount, transaction_date)
            
            # Update last transaction date
            account.last_transaction_date = transaction_date
            account.save()

    def create_deposit(self, account, balance, amount, timestamp):
        balance.balance_amount += amount
        balance.save()
        
        txn = Transaction.objects.create(
            account=account,
            transaction_type='Deposit',
            amount=amount,
            timestamp=timestamp
        )
        Deposit.objects.create(transaction=txn)
        
        self.stdout.write(self.style.SUCCESS(
            f'Created deposit of {amount} on {timestamp.strftime("%Y-%m-%d")}'
        ))

    def create_withdrawal(self, account, balance, amount, timestamp):
        balance.balance_amount -= amount
        balance.save()
        
        txn = Transaction.objects.create(
            account=account,
            transaction_type='Withdraw',
            amount=amount,
            timestamp=timestamp
        )
        Withdraw.objects.create(transaction=txn)
        
        self.stdout.write(self.style.SUCCESS(
            f'Created withdrawal of {amount} on {timestamp.strftime("%Y-%m-%d")}'
        ))

    def create_transfer(self, sender_account, recipient_account, sender_balance, amount, timestamp):
        # Get recipient balance
        recipient_balance = Balance.objects.get(account=recipient_account)
        
        # Update balances
        sender_balance.balance_amount -= amount
        sender_balance.save()
        recipient_balance.balance_amount += amount
        recipient_balance.save()
        
        # Create sender transaction (Transfer Out)
        sender_txn = Transaction.objects.create(
            account=sender_account,
            transaction_type='Transfer Out',
            amount=amount,
            timestamp=timestamp
        )
        TransferOut.objects.create(
            from_account=sender_account,
            to_account=recipient_account,
            amount=amount,
            recipient_account_number=recipient_account.account_number,
            timestamp=timestamp
        )
        
        # Create recipient transaction (Transfer In)
        recipient_txn = Transaction.objects.create(
            account=recipient_account,
            transaction_type='Transfer In',
            amount=amount,
            timestamp=timestamp
        )
        TransferIn.objects.create(
            from_account=sender_account,
            to_account=recipient_account,
            amount=amount,
            sender_account_number=sender_account.account_number,
            timestamp=timestamp
        )
        
        self.stdout.write(self.style.SUCCESS(
            f'Created transfer of {amount} to {recipient_account.account_number} on {timestamp.strftime("%Y-%m-%d")}'
        ))