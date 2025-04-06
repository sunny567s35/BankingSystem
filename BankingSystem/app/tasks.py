# accounts/tasks.py
from celery import shared_task
from decimal import Decimal
from django.utils import timezone
from .models import Account, Transaction, Balance, InterestTable
from datetime import datetime, timedelta

@shared_task
def calculate_hourly_interest():
    """
    Calculate hourly interest for savings accounts and update balances.
    """
    savings_accounts = Account.objects.filter(account_type__name='Savings')
    
    for account in savings_accounts:
        # Get the account's balance record
        balance = Balance.objects.get(account=account)
        
        # Calculate hourly interest (annual rate / 365 / 24)
        hourly_rate = Decimal(account.account_type.interest_rate) / Decimal('8760')  # 365*24
        interest_amount = Decimal(str(balance.balance_amount)) * hourly_rate
        
        # Update account balance
        balance.balance_amount += interest_amount
        balance.save()
        
        # Create interest transaction record
        Transaction.objects.create(
            account=account,
            transaction_type='Interest',
            amount=float(interest_amount),
        )
        
        # Update or create InterestTable record
        InterestTable.objects.update_or_create(
            account_type=account.account_type,
            defaults={
                'interest_rate': account.account_type.interest_rate,
            }
        )
    
    return f"Hourly interest calculated for {savings_accounts.count()} savings accounts"

@shared_task
def calculate_daily_interest_summary():
    """
    Generate a summary of interest credited in the past day.
    """
    savings_accounts = Account.objects.filter(account_type__name='Savings')
    start_date = timezone.now() - timedelta(hours=24)
    
    summary = []
    for account in savings_accounts:
        interest_transactions = Transaction.objects.filter(
            account=account,
            transaction_type='Interest',
            timestamp__gte=start_date
        )
        
        total_interest = sum(t.amount for t in interest_transactions)
        summary.append({
            'account_number': account.account_number,
            'customer_name': f"{account.customer.first_name} {account.customer.last_name}",
            'account_type': account.account_type.name,
            'interest_rate': account.account_type.interest_rate,
            'total_interest': total_interest,
            'current_balance': account.balance.balance_amount
        })
    
    return summary