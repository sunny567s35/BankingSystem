from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import models
from django.db import transaction


from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from django.shortcuts import redirect, render

def custom_admin_login(request):
    if request.user.is_authenticated:
        messages.error(request, "You are already logged in. Please logout to go to the Website Home Page.")
        return redirect(request.META.get("HTTP_REFERER", "custom_admin_dashboard"))  # Stay on the same page
    
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_superuser:
            login(request, user)
            return redirect("custom_admin_dashboard")
        else:
            messages.error(request, "Invalid credentials or not a superuser.")

    return render(request, "custom_admin/login.html")


def custom_admin_logout(request):
    logout(request)
    request.session.flush()  # Clears session data
    messages.success(request, "You have been logged out successfully.")
    return redirect("custom_admin_login")





from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Sum, Count
from app.models import Account, Transaction, Customer, Balance
from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType

@login_required
@user_passes_test(lambda u: u.is_staff)
def custom_admin_dashboard(request):
    # Get total accounts count
    total_accounts = Account.objects.count()
    
    # Get account type distribution using AccountType model
    account_types = AccountType.objects.annotate(
        account_count=Count('account_list')  # Using the related_name from your model
    )
    
    # Initialize counts
    savings_count = 0
    current_count = 0
    fd_count = 0
    
    # Count accounts by type
    for account_type in account_types:
        if 'savings' in account_type.name.lower():
            savings_count = account_type.account_count
        elif 'current' in account_type.name.lower():
            current_count = account_type.account_count
        elif 'fixed' in account_type.name.lower() or 'fd' in account_type.name.lower():
            fd_count = account_type.account_count
    
    # Get total balance from Balance table
    total_balance = Balance.objects.aggregate(
        total_balance=Sum('balance_amount')
    )['total_balance'] or 0.00
    
    # Get recent transactions with related data
    recent_transactions = Transaction.objects.select_related(
        'account',
        'account__customer'
    ).order_by('-timestamp')[:10]  # Increased to 10 for better display
    
    # Get recent admin activity from LogEntry
    content_type = ContentType.objects.get_for_model(Account)
    recent_activity = LogEntry.objects.filter(
        content_type=content_type
    ).select_related('user').order_by('-action_time')[:5]
    
    # Format activity logs for display
    formatted_activity = []
    for log in recent_activity:
        action_map = {
            1: ("plus-circle", "Created account", "primary"),
            2: ("edit", "Changed account", "warning"),
            3: ("trash", "Deleted account", "danger")
        }
        icon, action, color = action_map.get(log.action_flag, ("info-circle", "Performed action", "info"))
        
        # Try to get the account number if available
        try:
            account = Account.objects.get(id=log.object_id)
            details = f"Account: {account.account_number}"
        except Account.DoesNotExist:
            details = f"Account ID: {log.object_id}"
        
        formatted_activity.append({
            'icon': icon,
            'action': action,
            'details': details,
            'color': color,
            'timestamp': log.action_time,
            'admin_user': log.user.get_username()
        })
    
    return render(request, "custom_admin/dashboard.html", {
        "total_accounts": total_accounts,
        "total_balance": total_balance,
        "recent_transactions": recent_transactions,
        
        "recent_activity": formatted_activity,
        "account_types": account_types  # Pass all account types for reference
    })


from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db import transaction
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from django.http import JsonResponse
from django.urls import reverse
from app.models import (
    Account, Customer, Address,
    AccountType, Branch, Balance,
    Transaction, Deposit, generate_account_number
)

def new_account(request):
    # Ensure default account types and branches exist
    AccountType.objects.get_or_create(name='savings', defaults={'min_balance': 500.00, 'interest_rate': 0.50})
    AccountType.objects.get_or_create(name='current', defaults={'min_balance': 1000.00, 'interest_rate': 0.25})
    
    branches = ['main', 'north', 'south', 'east']
    for branch in branches:
        Branch.objects.get_or_create(branch_name=branch, defaults={'location': f"{branch.capitalize()} Branch"})

    if request.method == 'POST':
        try:
            with transaction.atomic():
                data = request.POST
                User = get_user_model()
                
                # Create User
                user = User.objects.create_user(
                    username=data.get('email'),
                    email=data.get('email'),
                    password=data.get('password'),
                    first_name=data.get('firstname'),
                    last_name=data.get('lastname')
                )

                # Create Customer
                customer = Customer.objects.create(
                    user=user,
                    first_name=data.get('firstname'),
                    last_name=data.get('lastname'),
                    email=data.get('email'),
                    phone=data.get('phone', ''),
                    date_of_birth=data.get('dob', None),
                    gender=data.get('gender', '').capitalize(),
                    occupation=data.get('occupation', ''),
                    income=float(data.get('income', 0))
                )

                # Create Address
                Address.objects.create(
                    customer=customer,
                    street=data.get('address', ''),
                    city=data.get('city', ''),
                    state=data.get('state', ''),
                    zip_code=data.get('zipcode', ''),
                    country=data.get('country', '')
                )

                # Generate account number
                account_number = generate_account_number()
                while Account.objects.filter(account_number=account_number).exists():
                    account_number = generate_account_number()

                # Create Account
                account = Account.objects.create(
                    customer=customer,
                    account_type=AccountType.objects.get(name=data.get('account_type').lower()),
                    branch=Branch.objects.get(branch_name=data.get('branch').lower()),
                    account_number=account_number,
                    password=make_password(data.get('password')),
                    last_transaction_date=timezone.now()
                )

                # Create Balance
                initial_balance = float(data.get('balance', 0))
                Balance.objects.create(
                    account=account,
                    balance_amount=initial_balance
                )

                # Create Transaction if initial deposit exists
                if initial_balance > 0:
                    transaction_obj = Transaction.objects.create(
                        account=account,
                        transaction_type='Deposit',
                        amount=initial_balance,
                        timestamp=timezone.now()
                    )
                    Deposit.objects.create(transaction=transaction_obj)

                # Return JSON response for API calls
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'status': 'success',
                        'account_number': account_number,
                        'message': 'Account created successfully',
                        'redirect_url': reverse('custom_admin_dashboard')  # Add redirect URL for AJAX
                    })

                # Return HTML response for normal browser requests
                messages.success(request, f'Account created successfully! Account Number: {account_number}')
                return redirect('custom_admin_dashboard')  # Changed from 'new_account' to 'dashboard'

        except Exception as e:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'error',
                    'message': str(e)
                }, status=400)
            messages.error(request, f'Error creating account: {str(e)}')
            return redirect('new_account')

    # GET request handling
    branches = Branch.objects.all()
    account_types = AccountType.objects.all()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'branches': [{'name': b.branch_name} for b in branches],
            'account_types': [{'name': at.name} for at in account_types]
        })
    
    return render(request, 'custom_admin/new_account.html', {
        'branches': branches,
        'account_types': account_types,
    })


from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from app.models import Account  # Adjust based on your actual model import
from django.contrib.auth.hashers import make_password


def manage_account(request):
    accounts = Account.objects.all()
    return render(request, 'custom_admin/manage_account.html', {'accounts': accounts})

from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.db import transaction
from app.models import Account, Customer

def delete_account(request, account_id):
    if request.method == "POST":
        try:
            with transaction.atomic():  # Ensures everything is deleted safely
                account = get_object_or_404(Account, id=account_id)
                customer = account.customer  # Get associated customer

                # Deleting the account will automatically delete related models due to CASCADE
                account.delete()

                # If the customer has no other accounts, delete the customer and their address
                if not customer.accounts.exists():
                    customer.delete()

                return JsonResponse({"success": True})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=400)

    return JsonResponse({"success": False}, status=400)


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.http import JsonResponse
from app.models import Account, Customer, Address, EditAccount
import json

@login_required
def edit_account(request, account_id):
    account = get_object_or_404(Account, id=account_id)
    customer = account.customer
    address = Address.objects.filter(customer=customer).first()
    
    if request.method == 'POST':
        try:
            changes = {}
            print("Starting account edit process...")  # Debug
            
            with transaction.atomic():
                # Debug: Print current customer values
                print(f"Current customer name: {customer.first_name} {customer.last_name}")
                
                # Track customer fields changes
                customer_fields = [ 'email', 'phone', 
                                  'date_of_birth', 'gender', 'occupation', 'income']
                
                for field in customer_fields:
                    if field in request.POST:
                        old_value = str(getattr(customer, field))
                        new_value = request.POST[field]
                        print(f"Processing {field}: old={old_value}, new={new_value}")  # Debug
                        
                        if old_value != new_value:
                            print(f"Change detected in {field}")  # Debug
                            setattr(customer, field, new_value)
                            changes[f'customer_{field}'] = {
                                'old': old_value,
                                'new': new_value
                            }
                
                # Debug: Print detected changes so far
                print(f"Changes detected: {changes}")
                
                # Track address fields changes
                address_fields = ['street', 'city', 'state', 'zip_code', 'country']
                if any(field in request.POST for field in address_fields):
                    if not address:
                        address = Address(customer=customer)
                        changes['address_created'] = True
                    
                    for field in address_fields:
                        if field in request.POST:
                            old_value = str(getattr(address, field, ''))
                            new_value = request.POST[field]
                            if old_value != new_value:
                                setattr(address, field, new_value)
                                changes[f'address_{field}'] = {
                                    'old': old_value,
                                    'new': new_value
                                }
                
                # Track password change
                if 'password' in request.POST and request.POST['password']:
                    account.password = make_password(request.POST['password'])
                    changes['password_changed'] = True
                
                # Debug: Print all changes before save
                print(f"All changes before save: {changes}")
                
                # Save all changes if there are any
                if changes:
                    customer.save()
                    print("Customer saved successfully")  # Debug
                    if address:
                        address.save()
                    account.save()
                    
                    # Create edit record
                    edit_record = EditAccount.objects.create(
                        account=account,
                        modified_by=request.user,
                        changes=changes,
                        notes=request.POST.get('notes', '')
                    )
                    print(f"EditAccount record created with ID: {edit_record.id}")  # Debug
                
                # Handle response
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'status': 'success',
                        'message': 'Account updated successfully',
                        'changes': changes,
                        'redirect_url': reverse('manage_account')
                    })
                
                messages.success(request, 'Account updated successfully')
                return redirect('manage_account')
        
        except Exception as e:
            print(f"Error during account edit: {str(e)}")  # Debug
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'error',
                    'message': str(e)
                }, status=400)
            messages.error(request, f'Error updating account: {str(e)}')
    
    # GET request handling
    return render(request, 'custom_admin/edit_account.html', {
        'account': account,
        'customer': customer,
        'address': address,
    })

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.db import transaction

@csrf_exempt
@require_http_methods(["POST"])
@login_required
def delete_account(request, account_id):
    try:
        with transaction.atomic():
            # Get account with all related data
            account = Account.objects.select_related(
                'customer', 
                'customer__user',
                'account_type',
                'branch'
            ).prefetch_related(
                'transactions',
                'transfers_in',
                'transfers_out'
            ).get(id=account_id)
            
            # First check if account is already in deleted table
            if DeletedAccount.objects.filter(account_number=account.account_number).exists():
                return JsonResponse({
                    'status': 'error',
                    'message': 'This account has already been deleted'
                }, status=400)
            
            customer = account.customer
            balance = account.balance.balance_amount if hasattr(account, 'balance') else 0
            
            # Create single DeletedAccount record
            deleted_account = DeletedAccount.objects.create(
                original_id=account.id,
                customer_name=f"{customer.first_name} {customer.last_name}",
                account_number=account.account_number,
                account_type=account.account_type.name,
                branch_name=account.branch.branch_name,
                balance_at_deletion=balance,
                closed_by=request.user,
                reason=request.POST.get('reason', 'No reason provided'),
                customer_email=customer.email,
                phone_number=customer.phone,
                last_transaction_date=account.last_transaction_date
            )
            
            # Deactivate user
            if customer.user:
                user = customer.user
                user.is_active = False
                user.username = f"deleted_{user.username}_{account.account_number[-4:]}"
                user.save()
            
            # Delete the account (this will cascade to related models)
            account.delete()
            
            # Check if customer has other accounts
            if not customer.accounts.exists():
                customer.delete()
            
            return JsonResponse({
                'status': 'success',
                'message': 'Account deleted successfully',
                'deleted_account_id': deleted_account.id
            })
    
    except Account.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Account not found'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)


def transactions_view(request):
    transactions = Transaction.objects.select_related('account').order_by('-timestamp')
    return render(request, 'custom_admin/transactions.html', {'transactions': transactions})



from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction as db_transaction
from django.utils import timezone
from decimal import Decimal, InvalidOperation
from app.models import Account, Balance, Customer, Deposit, Transaction
import logging

logger = logging.getLogger(__name__)

@csrf_exempt
def deposit_view(request):
    try:
        if request.method == "GET":
            # Handle AJAX request for account details
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and "account_number" in request.GET:
                account_number = request.GET.get("account_number", "").strip()
                logger.info(f"Account lookup request for: {account_number}")

                # Validate account number
                if not account_number:
                    return JsonResponse({
                        "status": "error", 
                        "message": "Account number is required."
                    }, status=400)

                if len(account_number) != 12:
                    return JsonResponse({
                        "status": "error",
                        "message": "Account number must be exactly 12 digits."
                    }, status=400)

                # Fetch account details
                try:
                    account = Account.objects.select_related('customer').get(account_number=account_number)
                    balance_record = Balance.objects.get(account=account)
                    
                    response_data = {
                        "status": "success",
                        "name": f"{account.customer.first_name} {account.customer.last_name}".strip(),
                        "balance": str(balance_record.balance_amount)
                    }
                    logger.info(f"Account details retrieved: {response_data}")
                    return JsonResponse(response_data)
                    
                except Account.DoesNotExist:
                    logger.warning(f"Account not found: {account_number}")
                    return JsonResponse({
                        "status": "error",
                        "message": "Account not found."
                    }, status=404)
                except Balance.DoesNotExist:
                    logger.warning(f"Balance record not found for account: {account_number}")
                    return JsonResponse({
                        "status": "error",
                        "message": "Account balance information missing."
                    }, status=404)

            # Regular GET request - render deposit page
            return render(request, "custom_admin/deposit.html")

        elif request.method == "POST":
            # Handle deposit transaction
            account_number = request.POST.get("account", "").strip()
            deposit_amount = request.POST.get("amount", "").strip()
            logger.info(f"Deposit initiated - Account: {account_number}, Amount: {deposit_amount}")

            # Validate inputs
            if not account_number or not deposit_amount:
                return JsonResponse({
                    "status": "error",
                    "message": "Both account number and amount are required."
                }, status=400)

            try:
                deposit_amount = Decimal(deposit_amount)
                if deposit_amount <= 0:
                    return JsonResponse({
                        "status": "error",
                        "message": "Deposit amount must be greater than zero."
                    }, status=400)
            except InvalidOperation:
                return JsonResponse({
                    "status": "error",
                    "message": "Invalid amount format. Please enter a valid number."
                }, status=400)

            # Process deposit
            with db_transaction.atomic():
                try:
                    account = Account.objects.select_for_update().get(account_number=account_number)
                    balance_record = Balance.objects.select_for_update().get(account=account)
                    
                    # Update account balance
                    new_balance = balance_record.balance_amount + deposit_amount
                    balance_record.balance_amount = new_balance
                    balance_record.save()
                    
                    # Update last transaction date on account
                    account.last_transaction_date = timezone.now()
                    account.save()

                    # Create transaction record
                    transaction_record = Transaction.objects.create(
                        account=account,
                        transaction_type='Deposit',
                        amount=deposit_amount,
                        timestamp=timezone.now()
                    )

                    # Create deposit record (only needs transaction reference)
                    Deposit.objects.create(
                        transaction=transaction_record
                    )

                    logger.info(f"Deposit successful. New balance: {new_balance}")
                    return JsonResponse({
                        "status": "success",
                        "new_balance": str(new_balance),
                        "message": "Deposit completed successfully."
                    })

                except Account.DoesNotExist:
                    logger.warning(f"Account not found during deposit: {account_number}")
                    return JsonResponse({
                        "status": "error",
                        "message": "Account not found."
                    }, status=404)
                except Balance.DoesNotExist:
                    logger.warning(f"Balance record not found during deposit: {account_number}")
                    return JsonResponse({
                        "status": "error",
                        "message": "Account balance information missing."
                    }, status=404)

    except Exception as e:
        logger.error(f"Unexpected error in deposit_view: {str(e)}", exc_info=True)
        return JsonResponse({
            "status": "error",
            "message": "An unexpected error occurred. Please try again later."
        }, status=500)

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction as db_transaction
from django.utils import timezone
from decimal import Decimal, InvalidOperation
from app.models import Account, Balance, Customer, Withdraw, Transaction
import logging

logger = logging.getLogger(__name__)

@csrf_exempt
def withdraw_view(request):
    try:
        if request.method == "GET":
            # Handle AJAX request for account details
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and "account_number" in request.GET:
                account_number = request.GET.get("account_number", "").strip()
                logger.info(f"Account lookup request for: {account_number}")

                # Validate account number
                if not account_number:
                    return JsonResponse({
                        "status": "error", 
                        "message": "Account number is required."
                    }, status=400)

                if len(account_number) != 12:
                    return JsonResponse({
                        "status": "error",
                        "message": "Account number must be exactly 12 digits."
                    }, status=400)

                # Fetch account details
                try:
                    account = Account.objects.select_related('customer').get(account_number=account_number)
                    balance_record = Balance.objects.get(account=account)
                    
                    response_data = {
                        "status": "success",
                        "name": f"{account.customer.first_name} {account.customer.last_name}".strip(),
                        "balance": str(balance_record.balance_amount)
                    }
                    logger.info(f"Account details retrieved: {response_data}")
                    return JsonResponse(response_data)
                    
                except Account.DoesNotExist:
                    logger.warning(f"Account not found: {account_number}")
                    return JsonResponse({
                        "status": "error",
                        "message": "Account not found."
                    }, status=404)
                except Balance.DoesNotExist:
                    logger.warning(f"Balance record not found for account: {account_number}")
                    return JsonResponse({
                        "status": "error",
                        "message": "Account balance information missing."
                    }, status=404)

            # Regular GET request - render withdraw page
            return render(request, "custom_admin/withdraw.html")

        elif request.method == "POST":
            # Handle withdraw transaction
            account_number = request.POST.get("account", "").strip()
            withdraw_amount = request.POST.get("amount", "").strip()
            logger.info(f"Withdraw initiated - Account: {account_number}, Amount: {withdraw_amount}")

            # Validate inputs
            if not account_number or not withdraw_amount:
                return JsonResponse({
                    "status": "error",
                    "message": "Both account number and amount are required."
                }, status=400)

            try:
                withdraw_amount = Decimal(withdraw_amount)
                if withdraw_amount <= 0:
                    return JsonResponse({
                        "status": "error",
                        "message": "Withdraw amount must be greater than zero."
                    }, status=400)
            except InvalidOperation:
                return JsonResponse({
                    "status": "error",
                    "message": "Invalid amount format. Please enter a valid number."
                }, status=400)

            # Process withdraw
            with db_transaction.atomic():
                try:
                    account = Account.objects.select_for_update().get(account_number=account_number)
                    balance_record = Balance.objects.select_for_update().get(account=account)
                    
                    # Check sufficient balance
                    if withdraw_amount > balance_record.balance_amount:
                        return JsonResponse({
                            "status": "error",
                            "message": "Insufficient funds for withdrawal."
                        }, status=400)

                    # Update account balance
                    new_balance = balance_record.balance_amount - withdraw_amount
                    balance_record.balance_amount = new_balance
                    balance_record.save()
                    
                    # Update last transaction date on account
                    account.last_transaction_date = timezone.now()
                    account.save()

                    # Create transaction record
                    transaction_record = Transaction.objects.create(
                        account=account,
                        transaction_type='Withdraw',
                        amount=withdraw_amount,
                        timestamp=timezone.now()
                    )

                    # Create withdraw record (only needs transaction reference)
                    Withdraw.objects.create(
                        transaction=transaction_record
                    )

                    logger.info(f"Withdraw successful. New balance: {new_balance}")
                    return JsonResponse({
                        "status": "success",
                        "new_balance": str(new_balance),
                        "message": "Withdrawal completed successfully."
                    })

                except Account.DoesNotExist:
                    logger.warning(f"Account not found during withdraw: {account_number}")
                    return JsonResponse({
                        "status": "error",
                        "message": "Account not found."
                    }, status=404)
                except Balance.DoesNotExist:
                    logger.warning(f"Balance record not found during withdraw: {account_number}")
                    return JsonResponse({
                        "status": "error",
                        "message": "Account balance information missing."
                    }, status=404)

    except Exception as e:
        logger.error(f"Unexpected error in withdraw_view: {str(e)}", exc_info=True)
        return JsonResponse({
            "status": "error",
            "message": "An unexpected error occurred. Please try again later."
        }, status=500)
    

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from decimal import Decimal, InvalidOperation
from app.models import Account, Balance, TransferIn, TransferOut, Transaction
import logging

logger = logging.getLogger(__name__)

@csrf_exempt
def transfer_view(request):
    try:
        if request.method == "GET":
            # Handle AJAX requests for account details
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and "account_number" in request.GET:
                account_number = request.GET.get("account_number", "").strip()
                logger.info(f"Account lookup request for: {account_number}")

                # Validate account number
                if not account_number:
                    return JsonResponse({
                        "status": "error", 
                        "message": "Account number is required."
                    }, status=400)

                if len(account_number) != 12:
                    return JsonResponse({
                        "status": "error",
                        "message": "Account number must be exactly 12 digits."
                    }, status=400)

                # Fetch account details
                try:
                    account = Account.objects.select_related('customer').get(account_number=account_number)
                    balance_record = account.balance  # Using OneToOne relation
                    
                    response_data = {
                        "status": "success",
                        "name": f"{account.customer.first_name} {account.customer.last_name}".strip(),
                        "balance": str(balance_record.balance_amount if balance_record else account.balance_amount)
                    }
                    logger.info(f"Account details retrieved: {response_data}")
                    return JsonResponse(response_data)
                    
                except Account.DoesNotExist:
                    logger.warning(f"Account not found: {account_number}")
                    return JsonResponse({
                        "status": "error",
                        "message": "Account not found."
                    }, status=404)

            # Regular GET request - render transfer page
            return render(request, "custom_admin/transfer.html")

        elif request.method == "POST":
            # Handle transfer transaction
            from_account_number = request.POST.get("from_account", "").strip()
            to_account_number = request.POST.get("to_account", "").strip()
            transfer_amount = request.POST.get("amount", "").strip()
            
            logger.info(f"Transfer initiated - From: {from_account_number}, To: {to_account_number}, Amount: {transfer_amount}")

            # Validate inputs
            if not from_account_number or not to_account_number or not transfer_amount:
                return JsonResponse({
                    "status": "error",
                    "message": "All fields are required."
                }, status=400)

            if from_account_number == to_account_number:
                return JsonResponse({
                    "status": "error",
                    "message": "Cannot transfer to the same account."
                }, status=400)

            try:
                transfer_amount = Decimal(transfer_amount)
                if transfer_amount <= 0:
                    return JsonResponse({
                        "status": "error",
                        "message": "Transfer amount must be greater than zero."
                    }, status=400)
            except InvalidOperation:
                return JsonResponse({
                    "status": "error",
                    "message": "Invalid amount format. Please enter a valid number."
                }, status=400)

            # Process transfer
            with transaction.atomic():
                try:
                    # Get and lock both accounts
                    from_account = Account.objects.select_for_update().get(account_number=from_account_number)
                    to_account = Account.objects.select_for_update().get(account_number=to_account_number)
                    
                    # Check sender's balance
                    from_balance = from_account.balance.balance_amount if hasattr(from_account, 'balance') else from_account.balance_amount
                    if transfer_amount > from_balance:
                        return JsonResponse({
                            "status": "error",
                            "message": "Insufficient funds for transfer."
                        }, status=400)

                    # Update sender's account
                    new_from_balance = from_balance - transfer_amount
                    from_account.balance_amount = new_from_balance
                    from_account.save()
                    
                    # Update sender's balance record
                    if hasattr(from_account, 'balance'):
                        from_account.balance.balance_amount = new_from_balance
                        from_account.balance.save()
                    else:
                        Balance.objects.create(
                            account=from_account,
                            balance_amount=new_from_balance
                        )

                    # Update recipient's account
                    to_balance = to_account.balance.balance_amount if hasattr(to_account, 'balance') else to_account.balance_amount
                    new_to_balance = to_balance + transfer_amount
                    to_account.balance_amount = new_to_balance
                    to_account.save()
                    
                    # Update recipient's balance record
                    if hasattr(to_account, 'balance'):
                        to_account.balance.balance_amount = new_to_balance
                        to_account.balance.save()
                    else:
                        Balance.objects.create(
                            account=to_account,
                            balance_amount=new_to_balance
                        )

                    # Create transfer records (updated to match new model fields)
                    TransferOut.objects.create(
                        from_account=from_account,
                        to_account=to_account,
                        amount=transfer_amount,
                        recipient_account_number=to_account_number
                    )

                    TransferIn.objects.create(
                        from_account=from_account,
                        to_account=to_account,
                        amount=transfer_amount,
                        sender_account_number=from_account_number
                    )

                    # Create transaction records
                    Transaction.objects.create(
                        account=from_account,
                        transaction_type='Transfer Out',
                        amount=transfer_amount
                    )

                    Transaction.objects.create(
                        account=to_account,
                        transaction_type='Transfer In',
                        amount=transfer_amount
                    )

                    logger.info(f"Transfer successful. New balances - From: {new_from_balance}, To: {new_to_balance}")
                    return JsonResponse({
                        "status": "success",
                        "message": f"Transfer of Rs.{transfer_amount} completed successfully.",
                        "new_balance": str(new_from_balance)
                    })

                except Account.DoesNotExist as e:
                    account_num = str(e).split()[0]
                    logger.warning(f"Account not found during transfer: {account_num}")
                    return JsonResponse({
                        "status": "error",
                        "message": f"Account not found: {account_num}"
                    }, status=404)

    except Exception as e:
        logger.error(f"Unexpected error in transfer_view: {str(e)}", exc_info=True)
        return JsonResponse({
            "status": "error",
            "message": "An unexpected error occurred. Please try again later."
        }, status=500)
    

from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from app.models import Announcements
from .forms import AnnouncementForm

def announcements_view(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        messages.error(request, "You don't have permission to access this page.")
        return redirect('custom_admin_login')
    
    announcements_list = Announcements.objects.filter(is_active=True).order_by('-created_at')
    paginator = Paginator(announcements_list, 10)  # Show 10 announcements per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'custom_admin/announcements.html', context)

def create_announcement(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        messages.error(request, "You don't have permission to access this page.")
        return redirect('custom_admin_login')
    
    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Announcement created successfully!')
            return redirect('announcements')
    else:
        form = AnnouncementForm()
    
    return render(request, 'custom_admin/create_announcement.html', {'form': form})

def delete_announcement(request, id):
    if not request.user.is_authenticated or not request.user.is_staff:
        messages.error(request, "You don't have permission to access this page.")
        return redirect('custom_admin_login')
    
    try:
        announcement = Announcements.objects.get(id=id)
        announcement.delete()
        messages.success(request, 'Announcement deleted successfully!')
    except Announcements.DoesNotExist:
        messages.error(request, 'Announcement not found.')
    
    return redirect('announcements')




from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from app.models import Ticket
from django.contrib import messages
from .forms import TicketResponseForm

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from app.models import Ticket
from .forms import TicketResponseForm

from django.core.exceptions import PermissionDenied

@login_required
def admin_tickets_list(request):
    # Superuser and staff can access
    if not (request.user.is_superuser or request.user.is_staff):
        raise PermissionDenied("You don't have permission to view this page.")
    
    tickets = Ticket.objects.all().order_by('-created_at')
    pending_count = Ticket.objects.filter(status='open').count()
    
    return render(request, 'custom_admin/tickets_list.html', {
        'tickets': tickets,
        'pending_tickets_count': pending_count,
        'is_admin': True
    })


@login_required
def admin_pending_tickets(request):
    if request.user.is_superuser:
        tickets = Ticket.objects.filter(status='open').order_by('-created_at')
    else:
        tickets = Ticket.objects.filter(customer__user=request.user, status='open').order_by('-created_at')

    pending_count = tickets.count()
    
    return render(request, 'custom_admin/tickets_list.html', {
        'tickets': tickets,
        'pending_tickets_count': pending_count,
        'show_pending_only': True
    })

@login_required
def admin_resolved_tickets(request):
    if request.user.is_superuser:
        tickets = Ticket.objects.filter(status='resolved').order_by('-created_at')
    else:
        tickets = Ticket.objects.filter(customer__user=request.user, status='resolved').order_by('-created_at')

    pending_count = Ticket.objects.filter(status='open').count()

    return render(request, 'custom_admin/tickets_list.html', {
        'tickets': tickets,
        'pending_tickets_count': pending_count,
        'show_resolved_only': True
    })

@login_required
def admin_ticket_detail(request, ticket_id):
    # Superuser and staff can access
    if not (request.user.is_superuser or request.user.is_staff):
        raise PermissionDenied("You don't have permission to view this page.")
    
    ticket = get_object_or_404(Ticket, id=ticket_id)
    
    if request.method == 'POST':
        form = TicketResponseForm(request.POST, instance=ticket)
        if form.is_valid():
            updated_ticket = form.save()
            messages.success(request, f'Ticket #{ticket.id} updated successfully!')
            return render(request, 'custom_admin/ticket_detail.html', {
                'ticket': ticket,
                'form': form,
                'is_admin': True
            })
    else:
        form = TicketResponseForm(instance=ticket)

    return render(request, 'custom_admin/ticket_detail.html', {
        'ticket': ticket,
        'form': form,
        'is_admin': True
    })
