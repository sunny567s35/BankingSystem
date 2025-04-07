from django.test import TestCase
from app.models import AccountType, Account, Balance, Branch
from app.tasks import calculate_30s_interest

class InterestTestCase(TestCase):
    def setUp(self):
        # Create required branch
        self.branch = Branch.objects.create(
            branch_name='Test Branch',
            location='Test Location'
        )
        
        self.acc_type = AccountType.objects.create(
            name='savings',
            interest_rate=4.0
        )
        
        self.account = Account.objects.create(
            account_number='TEST123',
            account_type=self.acc_type,
            branch=self.branch  # Add this line
        )
        
        Balance.objects.create(
            account=self.account,
            balance_amount=100000.00
        )
    
    def test_interest_calculation(self):
        result = calculate_30s_interest.delay().get(timeout=10)
        self.assertGreater(result['credited_accounts'], 0)