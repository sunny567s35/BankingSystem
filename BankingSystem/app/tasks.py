from celery import shared_task
from decimal import Decimal
from django.utils import timezone
from datetime import timedelta
from .models import Account, Transaction, Balance, InterestTable, AccountType
import logging
from django.db import transaction
from django.db.models import F




def debug_direct_calculation():
    """Bypass Celery to test the core logic"""
    from django.db import connection
    from decimal import Decimal
    from .models import Account, Balance, Transaction
    
    print("=== DIRECT CALCULATION TEST ===")
    
    # Raw SQL verification
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT COUNT(*) FROM app_account 
            JOIN app_accounttype ON app_account.account_type_id = app_accounttype.id
            WHERE LOWER(app_accounttype.name) = 'savings'
            AND app_account.branch_id IS NOT NULL
        """)
        count = cursor.fetchone()[0]
        print(f"Database confirms {count} valid savings accounts exist")
    
    # ORM verification
    accounts = Account.objects.filter(
        account_type__name__iexact='savings',
        branch__isnull=False
    ).select_related('balance')
    print(f"ORM Query returns {accounts.count()} accounts")
    
    # Test calculation on first account
    if accounts.exists():
        account = accounts.first()
        print(f"\nTesting with account {account.account_number}:")
        print(f"- Balance: {account.balance.balance_amount}")
        print(f"- Account Type: {account.account_type.name}")
        
        # Calculate interest
        rate = getattr(account.account_type.interesttable_set.first(), 'interest_rate', 
                      account.account_type.interest_rate)
        print(f"- Interest Rate: {rate}%")
        
        annual_rate = Decimal(str(rate))
        seconds_in_year = Decimal('31536000')
        interest = (Decimal(str(account.balance.balance_amount)) * annual_rate * Decimal('30') / (seconds_in_year * Decimal('100')))
        print(f"- 30-second interest: {interest}")
        
        return True
    return False


logger = logging.getLogger(__name__)
@shared_task(bind=True)
def calculate_30s_interest(self):
    try:
        logger.info("Starting interest calculation")
        
        # Explicit query with all required joins
        savings_accounts = Account.objects.filter(
            account_type__name__iexact='savings'
        ).select_related(
            'balance',
            'account_type',
            'branch'
        ).prefetch_related(
            'account_type__interesttable_set'
        )
        
        logger.info(f"Query will return {savings_accounts.count()} accounts")
        
        if not savings_accounts.exists():
            logger.error("CRITICAL: Query returned no accounts despite verification")
            # Emergency debug - check DB directly
            from django.db import connection
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT COUNT(*) FROM app_account 
                    JOIN app_accounttype ON app_account.account_type_id = app_accounttype.id
                    WHERE LOWER(app_accounttype.name) = 'savings'
                    AND app_account.branch_id IS NOT NULL
                """)
                db_count = cursor.fetchone()[0]
                logger.error(f"Direct DB count: {db_count}")
            return {'credited_accounts': 0, 'total_interest': '0.00'}
        
        credited_accounts = 0
        total_interest = Decimal('0.00')
        
        for account in savings_accounts:
            try:
                if not hasattr(account, 'balance'):
                    logger.warning(f"Skipping {account.account_number} - no balance")
                    continue
                    
                # Get interest rate - try both sources
                interest_rate = None
                if hasattr(account.account_type, 'interesttable_set'):
                    interest_table = account.account_type.interesttable_set.first()
                    if interest_table:
                        interest_rate = interest_table.interest_rate
                
                if interest_rate is None:
                    interest_rate = account.account_type.interest_rate
                
                # Calculation
                annual_rate = Decimal(str(interest_rate))
                seconds_in_year = Decimal('31536000')
                interest_amount = (
                    Decimal(str(account.balance.balance_amount)) * 
                    annual_rate * Decimal('30')
                ) / (seconds_in_year * Decimal('100'))
                
                if interest_amount < Decimal('0.01'):
                    continue
                
                # Update
                Balance.objects.filter(account=account).update(
                    balance_amount=F('balance_amount') + interest_amount
                )
                
                Transaction.objects.create(
                    account=account,
                    transaction_type='Interest',
                    amount=float(interest_amount),
                    timestamp=timezone.now()
                )
                
                credited_accounts += 1
                total_interest += interest_amount
                
            except Exception as e:
                logger.error(f"Failed on {account.account_number}: {str(e)}")
                continue
        
        logger.info(f"Completed: Credited {total_interest} to {credited_accounts} accounts")
        return {
            'credited_accounts': credited_accounts,
            'total_interest': str(total_interest)
        }
        
    except Exception as e:
        logger.error(f"TASK CRASHED: {str(e)}")
        raise self.retry(exc=e, countdown=60)
    



    