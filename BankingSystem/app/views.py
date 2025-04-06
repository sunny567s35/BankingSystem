import os
import random
from django.shortcuts import render , redirect
from django.http import HttpResponse, JsonResponse
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Account, Transaction, Customer, Address,Branch
from .serializers import AccountSerializer, TransactionSerializer, UserSerializer, CustomerSerializer,AddressSerializer
from django.shortcuts import get_object_or_404
import decimal
from django.core.mail import send_mail
import json
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from .models import Transaction
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sessions.models import Session
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import logout,authenticate, login as auth_login
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date, datetime, time, timedelta
from decimal import Decimal
from django.http import JsonResponse
from .models import Account
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db import transaction
from django.contrib.auth.hashers import make_password
from datetime import datetime
import uuid
import json
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from .models import (AccountType, Branch, Customer, Address, 
                     Account, Balance, Transaction, Deposit, Announcements)

from django.contrib.auth import authenticate, login as auth_login
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache
from django.http import JsonResponse
from django.contrib import messages
from django.shortcuts import redirect, render
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from .models import Account, Customer, Login
import json

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Transaction, Account, Balance  # Import your models
from django.urls import reverse
from django.http import JsonResponse
import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib import messages
from django.shortcuts import redirect
from .models import Customer, Account, Logout, Withdraw


from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from decimal import Decimal
from django.db import transaction as db_transaction
from django.core.mail import send_mail
from django.conf import settings
import json
from .models import (
    Account, Transaction, Balance, Customer,
    TransferIn, TransferOut, InterestTable  # Import the transfer models
)


import random
import json
from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache  # Use Django's cache system
from django.conf import settings


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Account, Customer, Balance


from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from decimal import Decimal
from .models import Customer, Account, Transaction, Balance, TransferIn, TransferOut


from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from decimal import Decimal
from .models import Account, Transaction, Balance, Customer
from django.core.mail import send_mail
from django.conf import settings
import json


from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import send_mail
from django.conf import settings

#send_transaction_email(request.user.email, "transfer", amount, sender_account.balance,sender_account.account_number,recipient_account.email,recipient_account.account_number)

from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from datetime import datetime, date



import json
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import JsonResponse
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ObjectDoesNotExist
from .models import Account, Balance

import logging


logger = logging.getLogger(__name__)

from django.utils import timezone
from datetime import datetime

def convert_to_naive_datetime(timestamp_str):
    # Convert the string to a timezone-aware datetime
    aware_datetime = datetime.fromisoformat(str(timestamp_str))
    # Convert to naive datetime
    return aware_datetime.astimezone(timezone.get_current_timezone()).replace(tzinfo=None)

# Add more views for withdrawal, transfer, and interest credit  
def home(request):
    if request.user.is_authenticated:
        # Instead of showing an error message, return user info
        return JsonResponse({
            'is_authenticated': True,
            'username': request.user.username,
        })
    # Render the React app's HTML
    return JsonResponse({
        'is_authenticated': False,
        'username': None,
    })  # Adjust the template name if necessary

# @api_view(['GET', 'POST'])
# def register(request):
#     if request.method == 'GET':
#         return render(request, 'register.html')

#     if request.method == 'POST':
#         # Debugging output
#         print(request.POST)  # Check what data is being submitted
#         # Fetch form data
#         first_name = request.POST.get('firstname')   #customer,user   
#         last_name = request.POST.get('lastname')     #customer,user
#         email = request.POST.get('email')              #customer,user
#         password = request.POST.get('password')             #customer,user
#         confirm_password = request.POST.get('confirm_password')         #customer,user
#         account_type = request.POST.get('account_type')             #customer,user
#         middlename = request.POST.get('middlename', '')             #customer,user
#         address_line = request.POST.get('address')             #Adress table
#         # country = request.POST.get('country')                         #Adress table  
#         # state = request.POST.get('state')                               #Adress table
#         # pincode = request.POST.get('pincode')                       #Adress tabl
#         if password != confirm_password:
#             return Response({'error': 'Passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)
#         username = f"{first_name}{last_name}".replace(" ", "").lower()
#         # Create User
#         user_serializer = UserSerializer(data={
#             'username': username,
#             'email': email,
#             'password': password,
#             'first_name': first_name,
#             'last_name': last_name
#         })
#                 # Create Employee and assign to default branch

        
        
#         if user_serializer.is_valid():
#             user = user_serializer.save()
#         else:
#             return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         default_branch = Branch.objects.first()
#         default_employee = Employee.objects.first() 
#         # customer = Customer.objects.create(
        
#         customer = Customer.objects.create(
#             user=user,
#             first_name=first_name,
#             last_name=last_name,
#             email=email,
            
#             employee=default_employee  # Set this if you have a specific employee to link
#         )
        
#         address = Address.objects.create(
#             customer=customer,
#             street=address_line,
#             # Add other address fields if necessary
#             city=request.POST.get('city', ''),
#             state=request.POST.get('state', ''),
#             zip_code=request.POST.get('pincode', ''),
#             country=request.POST.get('country', '')
#         )
#         # Create Account
#         account_serializer = AccountSerializer(data={
#             'customer':customer.id,
#             'opening_date':date.today(),
#             'branch':default_branch.id,       
#             'account_type': account_type,
#             'balance': 0.0,
#             'user': customer.id  # Linking User to Account
#         })
#         if account_serializer.is_valid():
#             account = account_serializer.save()
#         else:
#             return Response(account_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#         # Create Customer
#         # Send confirmation email
# #        send_registration_email(customer.email, customer.firstname)

#         # Alert the user
#         messages.success(request, 'User registered successfully')
#         return render(request, 'login.html', {'data': customer})
#     return render(request, 'register.html')
from django.views.decorators.csrf import ensure_csrf_cookie
from django.middleware.csrf import get_token

def get_csrf_token(request):
    return JsonResponse({'csrfToken': get_token(request)})

from django.contrib.auth import get_user_model
from django.db import transaction  # Fixed import
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.shortcuts import render, redirect
from datetime import datetime
import random
from .models import (AccountType, Branch, Customer, Address, 
                               Account, Balance, Transaction, Deposit)

@csrf_exempt  # Use this only for development; consider using CSRF tokens in production
def register(request):
    if request.method == 'POST':
        try:
            logger.info("Incoming registration data: %s", request.body)  # Log incoming data
            # Handle both form and API requests
            if request.content_type == 'application/json':
                data = json.loads(request.body)
            else:
                data = request.POST

            # Validation
            required_fields = ['email', 'password', 'confirm_password', 
                             'firstname', 'lastname']
            if missing := [f for f in required_fields if f not in data]:
                raise ValidationError(f"Missing fields: {', '.join(missing)}")

            if data['password'] != data['confirm_password']:
                raise ValidationError("Passwords don't match")

            if Customer.objects.filter(email=data['email']).exists():
                raise ValidationError("Email already registered")

            with transaction.atomic():  # ATOMIC TRANSACTION START
                # 1. Create User
                User = get_user_model()
                user = User.objects.create_user(
                    username=data['email'],
                    email=data['email'],
                    password=data['password'],
                    first_name=data['firstname'],
                    last_name=data['lastname']
                )

                # 2. Create Customer
                customer = Customer.objects.create(
                    user=user,
                    first_name=data['firstname'],
                    last_name=data['lastname'],
                    email=data['email'],
                    phone=data.get('phone'),
                    date_of_birth=data.get('dob'),
                    gender=data.get('gender', '').capitalize(),
                    occupation=data.get('occupation'),
                    income=float(data.get('income', 0.00))
                )

                # 3. Create Address (if data exists)
                if any(data.get(f) for f in ['address', 'city', 'state', 'zipcode', 'country']):
                    Address.objects.create(
                        customer=customer,
                        street=data.get('address', ''),
                        city=data.get('city', ''),
                        state=data.get('state', ''),
                        zip_code=data.get('zipcode', ''),
                        country=data.get('country', '')
                    )

                # 4. Get/Create AccountType and Branch
                acc_type_name = data.get('account_type', 'savings').lower()
                account_type = AccountType.objects.get_or_create(
                    name=acc_type_name,
                    defaults={
                        'min_balance': 500.00 if acc_type_name == 'savings' else 1000.00,
                        'interest_rate': 0.50 if acc_type_name == 'savings' else 0.25
                    }
                )[0]

                branch_name = data.get('branch', 'main').lower()
                branch = Branch.objects.get_or_create(
                    branch_name=branch_name,
                    defaults={'location': f"{branch_name.capitalize()} Branch"}
                )[0]

                # 5. Create Account (using the generate_account_number from model)
                account = Account.objects.create(
                    customer=customer,
                    account_type=account_type,
                    branch=branch,
                    # Let the model handle account number generation
                    password=make_password(data['password']),
                    last_transaction_date=datetime.now()
                )

                # Add account to branch's accounts ManyToMany
                branch.accounts.add(account)
                
                # Add account to account_type's accounts ManyToMany
                account_type.accounts.add(account)

                # 6. Create Balance Record
                initial_deposit = float(data.get('initial_deposit', 0.00))
                Balance.objects.create(
                    account=account,  # OneToOne link
                    balance_amount=initial_deposit
                )

                # 7. Create Transaction + Deposit if amount > 0
                if initial_deposit > 0:
                    txn = Transaction.objects.create(
                        account=account,
                        transaction_type='Deposit',
                        amount=initial_deposit
                    )
                    Deposit.objects.create(transaction=txn)

                # Success Response
                response_data = {
                    'account_number': account.account_number,
                    'customer_name': f"{customer.first_name} {customer.last_name}",
                    'balance': initial_deposit,
                    'branch': branch.branch_name
                }

                if request.content_type == 'application/json':
                    return JsonResponse({
                        'status': 'success',
                        'data': response_data
                    }, status=201)
                
                messages.success(request, 
                    f"Account created! Number: {account.account_number}")
                return redirect('login')

        except json.JSONDecodeError:
            error = "Invalid JSON data"
        except ValidationError as e:
            error = str(e)
        except Exception as e:
            logger.error("Error during registration: %s", str(e))  # Log the error
            error = f"Registration failed: {str(e)}"
            # Transaction will auto-rollback here

        # Error Response
        if request.content_type == 'application/json':
            return JsonResponse({'status': 'error', 'message': error}, status=400)
        
        messages.error(request, error)
        return redirect('/register')

    # GET Request - Show Form
    return render(request, '/register', {
        'account_types': AccountType.objects.all(),
        'branches': Branch.objects.all()
    })

from django.contrib.auth import authenticate, login as auth_login
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache
from django.http import JsonResponse
from django.contrib import messages
from django.shortcuts import redirect, render
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from .models import Account, Customer, Login
import json

@csrf_exempt
@api_view(['GET', 'POST'])
def login(request, username=None):
    # Handle active sessions
    if request.session.session_key:
        try:
            user_id = request.session.get('_auth_user_id')
            if user_id:
                user = User.objects.get(id=user_id)
                if request.content_type == 'application/json':
                    return JsonResponse({
                        'status': 'error',
                        'message': 'Already logged in',
                        'redirect': f'/dashboard/{user.username}/'
                    }, status=403)
                messages.error(request, "Already logged in")
                return redirect(f'/dashboard/{user.username}/')
        except User.DoesNotExist:
            pass

    # GET request - show form
    if request.method == 'GET':
        if request.content_type == 'application/json':
            return JsonResponse({'status': 'form_required'}, status=200)
        return render(request, 'login.html')

    # POST request - process login
    try:
        # Parse input data based on content type
        if request.content_type == 'application/json':
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')
            otp = data.get('otp')
        else:
            email = request.POST.get('email')
            password = request.POST.get('password')
            otp = request.POST.get('otp')

        # OTP Verification
        purpose = data.get('purpose', 'login')
        cached_otp = cache.get(f"otp_{email}_{purpose}")

        if cached_otp is None:
            response = {'status': 'error', 'message': 'Expired OTP'}
            if request.content_type == 'application/json':
                return JsonResponse(response, status=401)
            messages.error(request, response['message'])
            return redirect('/login/')

        # Account verification
        try:
            customer = Customer.objects.get(email=email)
            account = Account.objects.filter(customer=customer).first()
            user = authenticate(username=customer.user.username, password=password)
            
            if user is None:
                raise ValueError("Invalid credentials")

            # OTP Check
            if int(cached_otp) != int(otp):
                response = {'status': 'error', 'message': 'Invalid OTP'}
                if request.content_type == 'application/json':
                    return JsonResponse(response, status=401)
                messages.error(request, response['message'])
                return redirect('/login/')

            # Login user
            auth_login(request, user)
            
            # Record login
            Login.objects.create(
                customer=customer,
                customer_name=f"{customer.first_name} {customer.last_name}",
                account_number=account.account_number if account else None,
                ip_address=request.META.get('REMOTE_ADDR')
            )

            # Success response
            response = {
                'status': 'success',
                'message': f'Welcome {customer.first_name} {customer.last_name}',
                'redirect': f'/dashboard/{customer.user.username}/',
                'account_number': account.account_number if account else None
            }
            
            if request.content_type == 'application/json':
                return JsonResponse(response, status=200)
            
            messages.success(request, response['message'])
            return redirect(response['redirect'])

        except (Customer.DoesNotExist, ValueError) as e:
            response = {'status': 'error', 'message': 'Invalid credentials'}
            if request.content_type == 'application/json':
                return JsonResponse(response, status=401)
            messages.error(request, response['message'])
            return redirect('/login/')

    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)

def password_reset(request):
    if request.method != "POST":
        return JsonResponse({"error": "Method Not Allowed"}, status=405)

    try:
        data = json.loads(request.body)
        email = data.get("email")
        if not email:
            return JsonResponse({"error": "Email is required"}, status=400)

        user = User.objects.get(email=email)
        # Send password reset email here
        return JsonResponse({"message": "Password reset email sent"}, status=200)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

@login_required
def get_user(request):
    if request.user.is_authenticated:
        return JsonResponse({"user": request.user.username})  # Return username if authenticated
    return JsonResponse({"error": "User not authenticated"}, status=401)  # Return error if not logged in

@login_required
def view_tickets(request, username=None):
    if request.user.username != username:
        return JsonResponse({'error': "You can only view your own tickets."}, status=403)
    
    tickets = Ticket.objects.filter(customer=request.user.customer).order_by('-created_at')
    
    ticket_list = [
        {
            "id": ticket.id,
            "ticket_type_display": ticket.get_ticket_type_display(),
            "subject": ticket.subject,
            "status": ticket.status,
            "status_display": ticket.get_status_display(),
            "created_at": ticket.created_at.isoformat()
        }
        for ticket in tickets
    ]
    
    return JsonResponse({"tickets": ticket_list})

from django.http import JsonResponse
from .models import Ticket  # Adjust the import based on your project structure

def raise_ticket(request, username):
    if request.method == "POST":
        try:
            customer = get_object_or_404(Customer, email=username)
            data = json.loads(request.body)  # Parse JSON from React

            # Validate data
            ticket_type = data.get("ticket_type")
            subject = data.get("subject")
            description = data.get("description")

            if not all([ticket_type, subject, description]):
                return JsonResponse({"error": "All fields are required."}, status=400)

            # Save ticket
            ticket = Ticket.objects.create(
                customer=customer,
                ticket_type=ticket_type,
                subject=subject,
                description=description
            )

            return JsonResponse({"message": "Ticket created", "ticket_id": ticket.id}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)

@login_required
def user_ticket_detail(request, username, ticket_id):
    # Verify the requesting user matches the URL username
    if request.user.username != username:
        return JsonResponse({"error": "Unauthorized access"}, status=403)
    
    try:
        ticket = Ticket.objects.get(id=ticket_id, customer__user=request.user)
        # Convert ticket to dictionary
        ticket_data = {
            "id": ticket.id,
            "ticket_type": ticket.get_ticket_type_display(),
            "status": ticket.get_status_display(),
            "created_at": ticket.created_at.isoformat(),
            "updated_at": ticket.updated_at.isoformat(),
            "subject": ticket.subject,
            "description": ticket.description,
            "resolution": ticket.resolution,
            "user": {
                "username": ticket.customer.user.username
            }
        }
        return JsonResponse({"ticket": ticket_data})
    except Ticket.DoesNotExist:
        return JsonResponse({"error": "Ticket not found"}, status=404)

from django.http import JsonResponse
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json

@login_required
def change_password(request, username=None):
    if request.user.username != username:
        return JsonResponse({"error": "Unauthorized access"}, status=403)

    user = request.user

    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')

        if not check_password(old_password, user.password):
            return JsonResponse({"error": "Old password is incorrect"}, status=400)

        if new_password1 != new_password2:
            return JsonResponse({"error": "New passwords do not match"}, status=400)

        user.set_password(new_password1)
        user.save()

        update_session_auth_hash(request, user)  # Keep the user logged in
        messages.success(request, "Password changed successfully!")

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({"success": "Password changed successfully!"})
        else:
            return redirect('profile', username=username)

    return render(request, 'change_password.html')
    
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Transaction, Account, Balance, Announcements  # Import your models
from django.urls import reverse
from django.http import JsonResponse
import json
from django.core.serializers import serialize

@login_required
def dashboard(request, username=None):
    if not request.user.is_authenticated:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'status': 'unauthenticated',
                'redirect': '/login/'
            }, status=401)
        return redirect('/login/')
    print("_________Username_________", username)
    # If the logged-in user is an admin (superuser), show error on admin dashboard
    if request.user.is_superuser:
        return redirect(reverse("custom_admin_dashboard"))  # Redirect to admin dashboard
    
    # Ensure the logged-in user is accessing their own dashboard
    if request.user.username != username:
        messages.error(request, "You do not have permission to access this dashboard.")
        return redirect(f'/dashboard/{request.user.username}/')
    
    try:
        customer = request.user.customer
        print("_________Customer_________", customer)
        account = customer.accounts.first()  # Get first account of the customer
        print("_________Account_________", account)
        if not account:
            messages.error(request, "No account found!")
            return redirect('/login/')
            
        # Get current balance from Balance table
        current_balance = Balance.objects.get(account=account).balance_amount
        
        # Get last 5 transactions ordered by timestamp (newest first)
        transactions = Transaction.objects.filter(account=account).order_by('-timestamp')[:5]
        
        # We'll store the balance snapshots at each transaction point
        transaction_data = []
        
        # Get all balances at transaction points (we'll need to query the Balance table's history)
        # Since we don't have historical balances stored, we'll approximate by:
        # 1. Getting all transactions in chronological order
        # 2. Replaying them to calculate balances at each point
        
        # Get all transactions in chronological order
        all_transactions = Transaction.objects.filter(account=account).order_by('timestamp')
        
        # Initialize running balance
        running_balance = Decimal('0.00')
        
        # Create a dictionary to store balance after each transaction
        transaction_balances = {}
        
        for transaction in all_transactions:
            if transaction.transaction_type in ['Deposit', 'Transfer In', 'Interest']:
                running_balance += transaction.amount
            else:  # Withdraw or Transfer Out
                running_balance -= transaction.amount
            transaction_balances[transaction.id] = running_balance
        
        # Now prepare the data for the last 5 transactions
        for transaction in transactions:
            transaction_data.append({
                'timestamp': transaction.timestamp,
                'type': transaction.transaction_type,
                'amount': transaction.amount,
                'balance_after': transaction_balances.get(transaction.id, current_balance)
            })
        
    except Exception as e:
        messages.error(request, f"Error loading dashboard: {str(e)}")
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    announcements = Announcements.objects.filter(is_active=True).order_by('-created_at')[:3]
    print(announcements)
    serialized_announcements = serialize('json', announcements)
    print("_________Announcements_________", serialized_announcements)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'username': request.user.username,
            'balance': float(current_balance),
            'account': {
                'account_number': account.account_number,
                'balance': float(current_balance),
                'firstname': customer.first_name,
                'lastname': customer.last_name,
                'account_type': account.account_type.name
            },
            'transactions': [{
                'timestamp': t['timestamp'].isoformat(),
                'type': t['type'],
                'amount': float(t['amount']),
                'balance_after': float(t['balance_after'])
            } for t in transaction_data],
            'announcements': serialized_announcements,  
        })
    context = {
        'username': request.user.username,
        'account': {
            'account_number': account.account_number,
            'balance': current_balance,
            'firstname': customer.first_name,
            'lastname': customer.last_name,
            'account_type': account.account_type.name
        },
        'transactions': transaction_data
    }
    return JsonResponse(context)
@csrf_exempt
def forgot_password(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data.get("email")
            otp = data.get("otp")
            new_password = data.get("new_password")
            confirm_password = data.get("confirm_password")

            if not email or not otp or not new_password or not confirm_password:
                return JsonResponse({"success": False, "message": "All fields are required."})

            if new_password != confirm_password:
                return JsonResponse({"success": False, "message": "Passwords do not match."})

            cache_key = f"otp_{email}_password_reset"
            cached_otp = cache.get(cache_key)

            if not cached_otp:
                return JsonResponse({"success": False, "message": "OTP expired or not found."})

            if int(cached_otp) != int(otp):
                return JsonResponse({"success": False, "message": "Invalid OTP."})

            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return JsonResponse({"success": False, "message": "User not found."})

            user.set_password(new_password)
            user.save()

            # Clear OTP from cache
            cache.delete(cache_key)

            return JsonResponse({"success": True, "message": "Password reset successful!"})

        except Exception as e:
            return JsonResponse({"success": False, "message": f"Error: {str(e)}"})

    return JsonResponse({"success": False, "message": "Invalid request method."})
# @login_required
# @csrf_exempt
# def user_logout(request):
#     if not request.user.is_authenticated:
#         return JsonResponse({'status': 'error', 'message': 'User not authenticated'}, status=401)
#     try:
#         customer = Customer.objects.get(user=request.user)
#         account = Account.objects.filter(customer=customer).first()
        
#         # Record logout
#         Logout.objects.create(
#             customer=customer,
#             customer_name=f"{customer.first_name} {customer.last_name}",
#             account_number=account.account_number if account else None,
#             ip_address=request.META.get('REMOTE_ADDR')
#         )
#     except Customer.DoesNotExist:
#         pass

#     # Perform logout
#     auth_logout(request)
#     request.session.flush()
    
#     if request.content_type == 'application/json':
#         return JsonResponse({
#             'status': 'success',
#             'message': 'Logged out successfully',
#             'redirect': '/login/'
#         }, status=200)
    
#     messages.success(request, "Logged out successfully")
#     return redirect('/login/')

def user_logout(request):
    if request.method == "POST":
        logout(request)  # 🔴 This deletes the session
        return JsonResponse({"message": "Logged out successfully"}, status=200)
    
    return JsonResponse({"error": "Invalid request"}, status=400)

@login_required
def my_profile(request, username):
    print(f"Logged-in user: {request.user.username}, Requested: {username}")  # Debugging log

    # Ensure the user can only access their own profile
    if request.user.username != username:
        return JsonResponse({"error": "Unauthorized access"}, status=403)

    # Fetch the user's account
    account = get_object_or_404(
        Account.objects.select_related(
            'customer__user',
            'account_type',
            'branch',
            'balance'
        ),
        customer__user=request.user
    )

    # Check if the model has a 'created_at' field
    created_at = getattr(account, "created_at", None)

    # Return profile data as JSON
    return JsonResponse({
        "username": account.customer.user.username,
        "first_name": account.customer.user.first_name,
        "last_name": account.customer.user.last_name,
        "email": account.customer.user.email,
        "date_of_birth": account.customer.date_of_birth,
        "gender": account.customer.gender,
        "occupation": account.customer.occupation,
        "income": account.customer.income,
        "phone": account.customer.phone,
        "account_number": account.account_number,
        "branch": account.branch.branch_name,
        "account_type": account.account_type.name,
        "balance_amount": float(account.balance.balance_amount),  # Convert Decimal to float
        "created_at": created_at.strftime("%Y-%m-%d") if created_at else None,  # Handle missing field
    })


from django.db import transaction as db_transaction  # Renamed import to avoid conflict
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_http_methods

@require_http_methods(["GET", "POST"])
@ensure_csrf_cookie
@login_required
def withdraw(request, username=None):
    # Handle GET requests
    if request.method == 'GET':
        try:
            if request.user.username != username:
                return JsonResponse({
                    'status': 'error',
                    'message': 'You do not have permission to access this page.'
                }, status=403)
                
            customer = get_object_or_404(Customer, user=request.user)
            account = get_object_or_404(Account, customer=customer)
            balance = Balance.objects.get(account=account)
            
            return JsonResponse({
                'account_number': account.account_number,
                'current_balance': balance.balance_amount,
                'username': request.user.username
            })
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    # Handle AJAX POST requests
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            data = json.loads(request.body)
            amount = Decimal(data.get('amount', 0))
            
            # Validate user and account
            if request.user.username != username:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Permission denied'
                }, status=403)
                
            customer = get_object_or_404(Customer, user=request.user)
            account = get_object_or_404(Account, customer=customer)
            balance = Balance.objects.get(account=account)
            
            # Validate amount
            if amount <= 0:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Amount must be greater than zero'
                }, status=400)
                
            if amount > balance.balance_amount:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Insufficient balance'
                }, status=400)
            
            # Process withdrawal in atomic transaction
            with db_transaction.atomic():  # Using the renamed import
                # Update balance
                balance.balance_amount -= amount
                balance.save()
                
                # Create transaction record
                transaction = Transaction.objects.create(
                    account=account,
                    transaction_type='Withdraw',
                    amount=amount
                )
                
                # Create withdraw record
                Withdraw.objects.create(
                    transaction=transaction
                )
            
            # Send email notification
            send_mail(
                'Withdrawal Confirmation',
                f'You have successfully withdrawn Rs. {amount} from account {account.account_number}. '
                f'New balance: Rs. {balance.balance_amount}',
                settings.DEFAULT_FROM_EMAIL,
                [request.user.email],
                fail_silently=False,
            )
            
            return JsonResponse({
                'status': 'success',
                'message': f'Successfully withdrew Rs. {amount}',
                'new_balance': float(balance.balance_amount),
                'transaction_id': transaction.id
            })
            
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)


def validate_account(request, account_number):
    try:
        account = Account.objects.get(account_number=account_number)
        print("_________Account_________", account)
        return JsonResponse({
            'exists': True,
            'recipient_name': f"{account.customer.first_name} {account.customer.last_name}"
        })
    except Account.DoesNotExist:
        return JsonResponse({'exists': False})

@login_required
def transfer(request, username=None):
    if request.method == 'GET':
        try:
            customer = get_object_or_404(Customer, user=request.user)
            account = get_object_or_404(Account, customer=customer)
            balance = Balance.objects.get(account=account)
            
            return JsonResponse({
                'account_number': account.account_number,
                'current_balance': balance.balance_amount,
                'username': request.user.username
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            data = json.loads(request.body)
            amount = Decimal(data.get('amount', 0))
            recipient_account_number = data.get('recipient_account')
            
            # Validate user and account
            customer = get_object_or_404(Customer, user=request.user)
            sender_account = get_object_or_404(Account, customer=customer)
            sender_balance = Balance.objects.get(account=sender_account)
            
            # Validate recipient account
            try:
                recipient_account = Account.objects.get(account_number=recipient_account_number)
                recipient_balance = Balance.objects.get(account=recipient_account)
                recipient_name = f"{recipient_account.customer.first_name} {recipient_account.customer.last_name}"
            except Account.DoesNotExist:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Recipient account not found'
                }, status=400)
            
            # Validate amount
            if amount <= 0:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Amount must be greater than zero'
                }, status=400)
                
            if amount > sender_balance.balance_amount:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Insufficient balance'
                }, status=400)
                
            if sender_account.account_number == recipient_account.account_number:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Cannot transfer to yourself'
                }, status=400)
            
            # Process transfer in atomic transaction
            with db_transaction.atomic():
                # Update balances
                sender_balance.balance_amount -= amount
                sender_balance.save()
                recipient_balance.balance_amount += amount
                recipient_balance.save()
                
                # Create transaction records
                sender_transaction = Transaction.objects.create(
                    account=sender_account,
                    transaction_type='Transfer Out',
                    amount=amount
                )
                
                recipient_transaction = Transaction.objects.create(
                    account=recipient_account,
                    transaction_type='Transfer In',
                    amount=amount
                )
                
                # Create transfer records (without transaction field)
                TransferOut.objects.create(
                    from_account=sender_account,
                    to_account=recipient_account,
                    amount=amount,
                    recipient_account_number=recipient_account.account_number
                )
                
                TransferIn.objects.create(
                    from_account=sender_account,
                    to_account=recipient_account,
                    amount=amount,
                    sender_account_number=sender_account.account_number
                )
            
            # Send email notifications
            send_mail(
                'Transfer Confirmation',
                f'You have successfully transferred Rs. {amount} to {recipient_name} ({recipient_account.account_number}). '
                f'Your new balance: Rs. {sender_balance.balance_amount}',
                settings.DEFAULT_FROM_EMAIL,
                [request.user.email],
                fail_silently=False,
            )
            
            return JsonResponse({
                'status': 'success',
                'message': f'Successfully transferred Rs. {amount} to {recipient_name}',
                'new_balance': str(sender_balance.balance_amount),
                'transaction_id': sender_transaction.id,
                'recipient_name': recipient_name
            })
            
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

# accounts/views.py
@login_required
def interest(request, username=None):
    if request.user.username != username:
        return JsonResponse({
            'error': 'Permission denied',
            'redirect_username': request.user.username
        }, status=403)
    
    try:
        customer = request.user.customer
        account = customer.accounts.first()
        
        if not account:
            return JsonResponse({
                'error': 'No account found'
            }, status=404)
        
        # Get interest rate from account type
        if account.account_type.name == 'Savings':
            annual_rate = Decimal('6.0')  # 6%
            monthly_rate = Decimal('0.5')  # 0.5%
        else:
            annual_rate = Decimal('0.0')
            monthly_rate = Decimal('0.0')
        
        # Calculate projected interest
        current_balance = Balance.objects.get(account=account).balance_amount
        projected_interest = current_balance * (monthly_rate / Decimal('100'))
        
        return JsonResponse({
            'account': {
                'account_number': account.account_number,
                'account_type': {
                    'name': account.account_type.name
                }
            },
            'annual_rate': float(annual_rate),
            'projected_interest': float(projected_interest),
            'customer': {
                'first_name': customer.first_name,
                'last_name': customer.last_name,
                'username': request  .user.username  # Include username
            }
        })
        
    except Exception as e:
        return JsonResponse({
            'error': f"Error loading interest information: {str(e)}"
        }, status=500)

@login_required
def interest_summary(request, username=None):
    if request.user.username != username:
        return JsonResponse({
            'error': 'Permission denied',
            'redirect_username': request.user.username
        }, status=403)
    
    try:
        customer = request.user.customer
        account = customer.accounts.first()
        
        if not account:
            return JsonResponse({
                'error': 'No account found'
            }, status=404)
            
        # Get interest transactions for the last 24 hours
        start_date = timezone.now() - timedelta(hours=24)
        interest_transactions = Transaction.objects.filter(
            account=account,
            transaction_type='Interest',
            timestamp__gte=start_date
        ).order_by('-timestamp').values('amount', 'timestamp')
        
        # Get interest rate information from InterestTable
        interest_info = InterestTable.objects.filter(
            account_type  =account.account_type
        ).first()
        
        # Calculate total interest earned
        total_interest = sum(t.amount for t in interest_transactions)
        
        # Get current balance
        current_balance = Balance.objects.get(account=account).balance_amount
        
        # Calculate projected daily interest
        projected_daily_interest = Decimal('0.00')
        if account.account_type.name == 'Savings' and interest_info:
            daily_rate = interest_info.interest_rate / Decimal('365')
            projected_daily_interest = current_balance * daily_rate
            
        return JsonResponse({
            'account': {
                'account_number': account.account_number,
                'account_type': {
                    'name': account.account_type.name
                }
            },
            'interest_transactions': list(interest_transactions),
            'total_interest': float(total_interest),
            'projected_daily_interest': float(projected_daily_interest),
            'annual_rate': float(interest_info.interest_rate) if interest_info else 0.0,
            'customer': {
                'first_name': customer.first_name,
                'last_name': customer.last_name,
                'username': request.user.username  # Include username
            }
        })
        
    except Exception as e:
        return JsonResponse({
            'error': f"Error loading interest summary: {str(e)}"
        }, status=500)
    

    
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from decimal import Decimal
import logging
import json
from django.core.serializers.json import DjangoJSONEncoder

logger = logging.getLogger(__name__)

class CustomJSONEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'isoformat'):
            return obj.isoformat()
        elif isinstance(obj, Decimal):
            return float(obj)
        return super().default(obj)

@login_required
def statement(request, username=None):
    try:
        user = request.user
        customer = user.customer
        account = customer.accounts.first()

        if not account:
            return JsonResponse({'error': 'No account found'}, status=404)
        
        address = customer.customer_address.first()
        branch = account.branch
        account_type = account.account_type
        current_balance = Balance.objects.get(account=account).balance_amount

        # Mask sensitive data
        masked_phone = f"{customer.phone[:3]}*****{customer.phone[-2:]}" if customer.phone else "Not available"
        masked_email = f"{customer.email[:3]}****@{customer.email.split('@')[-1]}" if customer.email else "Not available"

        # Get all transactions
        all_transactions = Transaction.objects.filter(account=account).select_related(
            'account'
        ).order_by('timestamp')
        
        running_balance = Decimal('0.00')
        transaction_balances = {}
        serialized_transactions = []

        for transaction in all_transactions:
            # Calculate running balance
            if transaction.transaction_type in ['Deposit', 'Transfer In', 'Interest']:
                running_balance += transaction.amount
            elif transaction.transaction_type in ['Withdraw', 'Transfer Out']:
                running_balance -= transaction.amount
            transaction_balances[transaction.id] = running_balance

            # Create base transaction data
            transaction_data = {
                'id': transaction.id,
                'timestamp': transaction.timestamp,
                'transaction_type': transaction.transaction_type,
                'amount': transaction.amount,
                'description': transaction.transaction_type  # Default description
            }

            # Add transfer-specific details by querying related models
            if transaction.transaction_type == 'Transfer Out':
                try:
                    transfer_out = TransferOut.objects.filter(
                        from_account=account,
                        timestamp=transaction.timestamp,
                        amount=transaction.amount
                    ).first()
                    if transfer_out:
                        transaction_data['description'] = f"Sent to A/C {transfer_out.recipient_account_number}"
                except Exception as e:
                    logger.error(f"Error fetching transfer out: {str(e)}")
            
            elif transaction.transaction_type == 'Transfer In':
                try:
                    transfer_in = TransferIn.objects.filter(
                        to_account=account,
                        timestamp=transaction.timestamp,
                        amount=transaction.amount
                    ).first()
                    if transfer_in:
                        transaction_data['description'] = f"Received from A/C {transfer_in.sender_account_number}"
                except Exception as e:
                    logger.error(f"Error fetching transfer in: {str(e)}")

            serialized_transactions.append(transaction_data)

        # Sort transactions by timestamp (newest first)
        serialized_transactions.sort(key=lambda x: x['timestamp'], reverse=True)

        # Prepare response data
        response_data = {
            'customer': {
                'first_name': customer.first_name,
                'last_name': customer.last_name,
                'created_at': (customer.created_at),
                'phone': customer.phone,
                'email': customer.email
            },
            'address': {
                'street': address.street if address else None,
                'city': address.city if address else None,
                'state': address.state if address else None,
                'zip_code': address.zip_code if address else None,
                'country': address.country if address else None
            } if address else None,
            'last_activity': serialized_transactions[0]['timestamp'] if serialized_transactions else None,
            'account': {
                'account_number': account.account_number,
                'last_transaction_date': (serialized_transactions[0]['timestamp'])
            },
            'branch': {
                'branch_name': branch.branch_name,
                'location': branch.location
            },
            'account_type': {
                'name': account_type.name
            },
            'current_balance': current_balance,
            'transactions': serialized_transactions,
            'transaction_balances': [
                [str(tid), float(balance)] 
                for tid, balance in transaction_balances.items()
            ],
            'masked_phone': masked_phone,
            'masked_email': masked_email,
            'generation_date': timezone.now()
        }

        return JsonResponse(response_data, encoder=CustomJSONEncoder, safe=False)

    except Exception as e:
        logger.error(f"Error in statement view: {str(e)}", exc_info=True)
        return JsonResponse({
            'error': 'Internal server error',
            'details': str(e)
        }, status=500)

@require_http_methods(["GET", "POST"])
@ensure_csrf_cookie
@login_required
def deposit(request, username):
    if request.method == 'GET':
        try:
            customer = Customer.objects.get(user__username=username)
            account = Account.objects.get(customer=customer)
            balance = Balance.objects.get(account=account)
            
            return JsonResponse({
                'account_number': account.account_number,
                'current_balance': float(balance.balance_amount),
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            amount = Decimal(data.get('amount', 0))
            
            if amount <= 0:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Amount must be greater than zero'
                }, status=400)
            
            customer = Customer.objects.get(user__username=username)
            account = Account.objects.get(customer=customer)
            balance = Balance.objects.get(account=account)
            
            # Update balance
            balance.balance_amount += amount
            balance.save()
            
            # Create transaction record
            transaction = Transaction.objects.create(
                account=account,
                transaction_type='Deposit',
                amount=amount
            )
                        # Send email notification
            send_mail(
                'Deposit Confirmation',
                f'You have successfully deposited Rs. {amount} into account {account.account_number}. '
                f'New balance: Rs. {balance.balance_amount}',
                settings.DEFAULT_FROM_EMAIL,
                [request.user.email],
                fail_silently=False,
            )
            
            return JsonResponse({
                'status': 'success',
                'message': f'Successfully deposited Rs. {amount}',
                'new_balance': float(balance.balance_amount),
                'transaction_id': transaction.id
            })
            
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)

import random
import json
from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache  # Use Django's cache system
from django.conf import settings

@csrf_exempt
def send_otp(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data.get("email")
            purpose = data.get("purpose", "login")  # default: login

            if not email:
                return JsonResponse({"success": False, "message": "Email is required."})

            otp = random.randint(100000, 999999)
            subject = "Your OTP Code"
            banner_image_url = "https://i.imgur.com/PTL553r.png"

            message = f"""<html>
                            <body style="font-family: Arial, sans-serif; text-align: center; color: #333;">
                                <center><img src="{banner_image_url}" alt="Banner" width="100%"></center>
                                <h2 style="color: #0275d8;">Email Verification OTP</h2>
                                <p style="font-size: 18px;">Your OTP is <strong style="color: red; font-size: 22px;">{otp}</strong></p>
                                <p>This OTP is valid for <strong>5 minutes</strong>.</p>
                                <hr><p>If you did not request this OTP, please ignore this email.</p>
                                <p>Warm Regards,<br><strong style="color: #5F259F;">Mthree Banking</strong></p>
                            </body></html>"""

            from_email = settings.EMAIL_HOST_USER
            recipient_list = [email]
            
            # 🔁 Save with purpose-based cache key
            cache_key = f"otp_{email}_{purpose}"
            cache.set(cache_key, otp, timeout=300)
            
            print(f"[SEND OTP] Cache Key: {cache_key} | OTP: {otp}")
            try:
                email_obj = EmailMultiAlternatives(subject, message, from_email, recipient_list)
                email_obj.attach_alternative(message, "text/html")
                email_obj.send()
            except Exception as e:
                print(f"Failed to send email: {e}")

            return JsonResponse({"success": True, "message": "OTP sent successfully!"})

        except Exception as e:
            return JsonResponse({"success": False, "message": f"Error: {str(e)}"})

    return JsonResponse({"success": False, "message": "Invalid request."})

@login_required
@ensure_csrf_cookie
def verify_balance_password(request):
    if request.method != "POST":
        return JsonResponse({
            "success": False, 
            "message": "Only POST requests are allowed."
        }, status=405)

    try:
        data = json.loads(request.body)
        password = data.get("password")
        
        if not password:
            return JsonResponse({
                "success": False,
                "message": "Password is required."
            }, status=400)

        # Verify the user's password
        if not check_password(password, request.user.password):
            return JsonResponse({
                "success": False,
                "message": "Invalid password. Please try again."
            }, status=401)

        # Get the account and balance information
        try:
            account = Account.objects.get(customer__user=request.user)
            balance = Balance.objects.get(account=account)
            
            return JsonResponse({
                "success": True,
                "message": "Password verified successfully.",
                "balance": str(balance.balance_amount),
                "account_number": account.account_number,
                "account_type": account.account_type.name,
                "currency": "₹"  # Assuming Indian Rupees based on your template
            })
            
        except ObjectDoesNotExist:
            return JsonResponse({
                "success": False,
                "message": "Account information not found."
            }, status=404)

    except json.JSONDecodeError:
        return JsonResponse({
            "success": False,
            "message": "Invalid JSON data."
        }, status=400)
        
    except Exception as e:
        # Log the error for debugging
        print(f"Error in verify_balance_password: {str(e)}")
        return JsonResponse({
            "success": False,
            "message": "An unexpected error occurred."
        }, status=500)

@csrf_exempt
def verify_otp(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data.get("email")
            otp = data.get("otp")
            purpose = data.get("purpose", "login")  # default purpose is login

            if not email or not otp:
                return JsonResponse({"success": False, "message": "Email and OTP are required."})

            # 🔁 Use same purpose-based cache key
            cache_key = f"otp_{email}_{purpose}"
            cached_otp = cache.get(cache_key)

            if not cached_otp:
                return JsonResponse({
                    "success": False, 
                    "message": "OTP expired or not found. Please request a new one."
                })

            if str(cached_otp) != str(otp).strip():
                return JsonResponse({
                    "success": False, 
                    "message": "Invalid OTP. Please try again."
                })

            return JsonResponse({
                "success": True,
                "message": "OTP verified successfully."
            })

        except Exception as e:
            return JsonResponse({
                "success": False, 
                "message": f"Error verifying OTP: {str(e)}"
            })

    return JsonResponse({
        "success": False, 
        "message": "Invalid request method."
    })


from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from io import BytesIO
from django.utils import timezone
from decimal import Decimal
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from datetime import timedelta  # Import timedelta

from django.utils import timezone
from datetime import datetime

def format_date(date_string):
    if not date_string:
        return ''
    
    # Convert to datetime object if it's a string
    if isinstance(date_string, str):
        try:
            date_obj = datetime.fromisoformat(date_string.replace('Z', '+00:00'))
        except ValueError:
            return ''
    else:
        date_obj = date_string
    
    # Format the date to match the frontend display
    return date_obj.strftime('%d %b %Y, %I:%M %p')  # e.g. "03 Apr 2025, 06:53 PM"

import pytz
from django.utils import timezone

import pytz
from datetime import datetime
import tzlocal  # Requires pip install tzlocal

import pytz
from django.utils import timezone
from datetime import datetime

def convert_to_localtime(utctime):
    """
    Force conversion to Indian Standard Time (IST)
    Format: DD/MM/YYYY HH:MM (24-hour format)
    """
    # Define India timezone
    india_tz = pytz.timezone('Asia/Kolkata')
    
    # If datetime is naive (no timezone), assume it's UTC
    if not utctime.tzinfo:
        utctime = pytz.UTC.localize(utctime)
    # If datetime has timezone, convert to UTC first
    else:
        utctime = utctime.astimezone(pytz.UTC)
    
    # Convert to India time
    ist_time = utctime.astimezone(india_tz)
    
    # Format as Indian date/time (24-hour format)
    return ist_time.strftime('%d/%m/%Y %H:%M')

@login_required
def download_statement_pdf(request):
    try:
        # Create a buffer for the PDF
        buffer = BytesIO()
        
        # Create the PDF object with smaller margins
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=36,
            leftMargin=36,
            topMargin=36,
            bottomMargin=36
        )
        
        # Get all necessary data
        customer = request.user.customer
        account = customer.accounts.first()
        address = customer.customer_address.first()
        branch = account.branch
        account_type = account.account_type
        current_balance = Balance.objects.get(account=account).balance_amount
        
        # Mask sensitive information
        masked_phone = f"{customer.phone[:3]}*****{customer.phone[-2:]}" if customer.phone else "Not available"
        masked_email = f"{customer.email[:3]}****@{customer.email.split('@')[-1]}" if customer.email else "Not available"

        # Get all transactions with running balances
        all_transactions = Transaction.objects.filter(account=account).select_related('account').order_by('timestamp')
        running_balance = Decimal('0.00')
        transaction_balances = {}
        serialized_transactions = []

        for transaction in all_transactions:
            # Calculate running balance
            if transaction.transaction_type in ['Deposit', 'Transfer In', 'Interest']:
                running_balance += transaction.amount
            elif transaction.transaction_type in ['Withdraw', 'Transfer Out']:
                running_balance -= transaction.amount
            transaction_balances[transaction.id] = running_balance

            # Create base transaction data
            transaction_data = {
                'id': transaction.id,
                'timestamp': transaction.timestamp,
                'transaction_type': transaction.transaction_type,
                'amount': transaction.amount,
                'description': transaction.transaction_type  # Default description
            }

            # Add transfer-specific details by querying related models
            if transaction.transaction_type == 'Transfer Out':
                try:
                    transfer_out = TransferOut.objects.filter(
                        from_account=account,
                        timestamp=transaction.timestamp,
                        amount=transaction.amount
                    ).first()
                    if transfer_out:
                        transaction_data['description'] = f"Sent to A/C {transfer_out.recipient_account_number}"
                except Exception as e:
                    logger.error(f"Error fetching transfer out: {str(e)}")
            
            elif transaction.transaction_type == 'Transfer In':
                try:
                    transfer_in = TransferIn.objects.filter(
                        to_account=account,
                        timestamp=transaction.timestamp,
                        amount=transaction.amount
                    ).first()
                    if transfer_in:
                        transaction_data['description'] = f"Received from A/C {transfer_in.sender_account_number}"
                except Exception as e:
                    logger.error(f"Error fetching transfer in: {str(e)}")

            serialized_transactions.append(transaction_data)

        # Sort transactions by timestamp (newest first)
        serialized_transactions.sort(key=lambda x: x['timestamp'], reverse=True)
        
        # Prepare story (content) for PDF
        styles = getSampleStyleSheet()
        
        # Custom styles
        bank_title_style = ParagraphStyle(
            'BankTitle',
            parent=styles['Heading1'],
            fontSize=18,
            alignment=TA_CENTER,
            spaceAfter=10,
            textColor=colors.HexColor('#0d6efd'),
            fontName='Helvetica-Bold'
        )
        
        section_title_style = ParagraphStyle(
            'SectionTitle',
            parent=styles['Heading2'],
            fontSize=14,
            spaceAfter=10,
            textColor=colors.HexColor('#343a40'),
            fontName='Helvetica-Bold'
        )
        
        footer_style = ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=8,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#6c757d')
        )
        
        story = []
        
        # Bank Header
        story.append(Paragraph("Mthree Bank", bank_title_style))
        story.append(Paragraph("Customer Account Statement", section_title_style))
        story.append(Spacer(1, 20))
        
        # Customer and Account Information - Side by Side
        customer_info = [
            ["Customer Information", ""],
            ["Name:", f"{customer.first_name} {customer.last_name}"],
            ["Address:", f"{address.street if address else ''}"],
            ["", f"{address.city if address else ''}, {address.state if address else ''}"],
            ["", f"{address.zip_code if address else ''}, {address.country if address else ''}"],
            ["Mobile:", masked_phone],
            ["Email:", masked_email],
            ["Member Since:", convert_to_localtime(customer.created_at)]
        ]
        
        # Get last activity date
        last_activity = serialized_transactions[0]['timestamp'] if serialized_transactions else None
        
        account_info = [
            ["Account Information", ""],
            ["Account Number:", account.account_number],
            ["", ""],  # Spacer
            ["Branch:", f"{branch.branch_name}"],  # Branch location on new line
            ["", f"{branch.location}"],  # Branch location on new line
            ["Account Type:", account_type.name],
            ["", ""],  # Spacer
            ["Last Activity:", convert_to_localtime(last_activity)]
        ]
        
        # Create tables with improved styling
        customer_table = Table(customer_info, colWidths=[1.5*inch, 4*inch])
        account_table = Table(account_info, colWidths=[1.5*inch, 4*inch])
        
        table_style = TableStyle([
            ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
            ('FONTSIZE', (0,0), (-1,-1), 10),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
            ('SPAN', (0,0), (1,0)),  # Span section headers
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f8f9fa')),
            ('TEXTCOLOR', (0,0), (-1,0), colors.HexColor('#212529')),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ])
        
        customer_table.setStyle(table_style)
        account_table.setStyle(table_style)
        
        # Combine into side-by-side layout
        combined_table = Table([[customer_table, Spacer(0.5*inch, 0), account_table]], 
                              colWidths=[3.5*inch, 0.5*inch, 3.5*inch])
        story.append(combined_table)
        story.append(Spacer(1, 20))
        
        # Transaction History
        story.append(Paragraph("Transaction History", section_title_style))
        story.append(Spacer(1, 10))
        
        # Prepare transaction data
        transaction_data = [
            ["Date", "ID", "Description", "Amount (Rs.)", "Balance (Rs.)"]
        ]
        
        for transaction in serialized_transactions:
            # Format amount with color
            amount = transaction['amount']
            if transaction['transaction_type'] in ['Withdraw', 'Transfer Out']:
                formatted_amount = f"<font color='red'>-{amount:.2f}</font>"
            else:
                formatted_amount = f"<font color='green'>+{amount:.2f}</font>"
            formatted_date = convert_to_localtime(transaction['timestamp'])
            transaction_data.append([
                formatted_date,
                f"TX{transaction['id']:06d}",
                transaction['description'],
                Paragraph(formatted_amount, styles['Normal']),
                f"{transaction_balances.get(transaction['id'], current_balance):.2f}"
            ])
        
        # Add current balance row
        transaction_data.append([
            "", "", "Current Balance:", f"Rs. {current_balance:.2f}"
        ])
        
        # Create transaction table with improved styling
        transaction_table = Table(
            transaction_data,
            colWidths=[1.2*inch, 0.7*inch, 2.8*inch, 1*inch, 1*inch],
            repeatRows=1
        )
        
        transaction_table.setStyle(TableStyle([
            ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
            ('FONTSIZE', (0,0), (-1,0), 10),
            ('FONTSIZE', (0,1), (-1,-1), 9),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('ALIGN', (3,0), (-1,-1), 'RIGHT'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('INNERGRID', (0,0), (-1,-2), 0.5, colors.HexColor('#dee2e6')),
            ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#adb5bd')),
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#343a40')),
            ('TEXTCOLOR', (0,0), (-1,0), colors.HexColor('#ffffff')),
            ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor('#e9ecef')),
            ('SPAN', (0,-1), (2,-1)),
            ('ALIGN', (0,-1), (2,-1), 'RIGHT'),
            ('FONTNAME', (0,-1), (-1,-1), 'Helvetica-Bold'),
        ]))
        
        story.append(transaction_table)
        story.append(Spacer(1, 20))
        
        # Footer
        story.append(Paragraph("This is an electronically generated statement. No signature is required.", footer_style))
        story.append(Paragraph("Mthree Bank • Customer Service: 1800-123-4567 • www.mthreebank.com", footer_style))
        
        # Build PDF
        doc.build(story)
        
        # Get PDF value and close buffer
        pdf = buffer.getvalue()
        buffer.close()
        
        # Create HTTP response
        response = HttpResponse(
            content_type='application/pdf',
            headers={
                'Content-Disposition': 'attachment; filename="Mthree_Bank_Statement.pdf"',
                'Content-Length': str(len(pdf))
            }
        )
        response.write(pdf)
        return response
        
    except Exception as e:
        import logging
        logging.error(f"PDF generation failed: {str(e)}")
        return JsonResponse({
            'error': 'Failed to generate PDF',
            'details': str(e)
        }, status=500)
        
@login_required
def about(request):
    return render(request, 'about.html')

@login_required
def setting(request,username=None):
    if request.user.username != username:
        messages.error(request, "You do not have permission to access this page.")
        return redirect(f'/dashboard/{request.user.username}/')
    return render(request, 'settings.html',{'username':username})


from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import send_mail
from django.conf import settings

#send_transaction_email(request.user.email, "transfer", amount, sender_account.balance,sender_account.account_number,recipient_account.email,recipient_account.account_number)

from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from datetime import datetime, date

def send_transaction_email(user_email, user_account_number, transaction_type, amount, user_balance, recipient_email=None, recipient_account_number=None, recipient_balance=0):
    subject = f"{transaction_type.capitalize()} Confirmation"
    print("_________Sending Mail to_________", user_email)
    print("_________Transaction Type_________", transaction_type)
    user_account_number="XXXXX"+user_account_number[-4:]
    print("_________User Account Number_________", user_account_number)
    if recipient_account_number:
        recipient_account_number="XXXXX"+recipient_account_number[-3:]
        print("_________Recipient Account Number_________", recipient_account_number)
    
    # Replace with your actual domain (Django does not serve static files in emails automatically)
    site_url = "https://yourbank.com"  # Change this to your real domain
    # banner_image_url = f"/static/images/banner.jpg"  # Full URL to the image
    # banner_path = os.path.join(settings.BASE_DIR, "static/images/banner.jpg")
    banner_image_url = "https://i.imgur.com/PTL553r.png"  # Imgur banner image


    timestamp = f"{date.today()} at {datetime.now().strftime('%H:%M:%S')}"

    # HTML Email Template
    html_message = f"""
        <html>
        <body style="font-family: Arial, sans-serif; color: #333;">
            <center><img src="{banner_image_url}" width="100%" alt="Bank Banner"></center>
            <h2 style="color: #0275d8;">❗️{transaction_type.capitalize()} Notification</h2>
            <h4>Dear Customer,</h4>
    """

    if transaction_type == "deposit":
        html_message += f"""
            <p>Your deposit of <strong style="color: green;">Rs.{amount:.2f}</strong> into account <strong>**{user_account_number}**</strong> was successful on <strong>{timestamp}</strong>.</p>
            <p>Your updated account balance is <strong>Rs.{user_balance:.2f}</strong>.</p>
        """
    
    elif transaction_type == "withdrawal":
        html_message += f"""
            <p><strong style="color: red;">Rs.{amount:.2f}</strong> has been withdrawn from your account <strong>**{user_account_number}**</strong> on <strong>{timestamp}</strong>.</p>
            <p>Your updated account balance is <strong>Rs.{user_balance:.2f}</strong>.</p>
        """
    
    elif transaction_type == "transfer":
        print("_________Transfer_________", user_account_number, recipient_account_number)
        
        # Debit Email (Sender)
        debit_html = f"""
            <html>
            <body style="font-family: Arial, sans-serif; color: #333;">
                <!-- <center><img src="{banner_image_url}" width="100%" alt="Bank Banner"></center> 
                <h2 style="color: #f0ad4e;">Transfer Notification</h2> -->
                <p><strong style="color: red;">Rs.{amount:.2f}</strong> has been debited from your account <strong>**{user_account_number}**</strong> to account <strong>**{recipient_account_number}**</strong> on <strong>{timestamp}</strong>.</p>
                <p>Your updated account balance is <strong>Rs.{user_balance:.2f}</strong>.</p>
                <p style="color: red;">If you did not authorize this transaction, please <a href="{site_url}/support">contact support</a> immediately.</p>
                <p>Warm Regards,<br><strong style="color: #5F259F;">Mthree Banking</strong></p>
            </body>
            </html>
        """
        
        # Credit Email (Recipient)
        credit_html = f"""
            <html>
            <body style="font-family: Arial, sans-serif; color: #333;">
                <!-- <center><img src="{banner_image_url}" width="100%" alt="Bank Banner"></center> 
                <h2 style="color: #5cb85c;">Credit Notification</h2> -->
                <p><strong style="color: green;">Rs.{amount:.2f}</strong> has been credited to your account <strong>**{recipient_account_number}**</strong> from account <strong>**{user_account_number}**</strong> on <strong>{timestamp}</strong>.</p>
                <p>Your updated account balance is <strong>Rs.{recipient_balance:.2f}</strong>.</p>
                <p style="color: red;">If you did not authorize this transaction, please <a href="{site_url}/support">contact support</a> immediately.</p>
                <p>Warm Regards,<br><strong style="color: #5F259F;">Mthree Banking</strong></p>
            </body>
            </html>
        """
        debit_html=html_message+debit_html
        credit_html=html_message+credit_html
        # Sending Emails
        from_email = settings.EMAIL_HOST_USER
        try:
            # Send debit email
            debit_email = EmailMultiAlternatives(subject, debit_html, from_email, [user_email])
            debit_email.attach_alternative(debit_html, "text/html")
            debit_email.send()
            print(f"HTML Email sent successfully for debit to {user_email}")

            # Send credit email
            credit_email = EmailMultiAlternatives(subject, credit_html, from_email, [recipient_email])
            credit_email.attach_alternative(credit_html, "text/html")
            credit_email.send()
            print(f"HTML Email sent successfully for credit to {recipient_email}")
        except Exception as e:
            print(f"Failed to send email: {str(e)}")

        return  # Exit function after transfer emails are sent

    # Common HTML Footer
    html_message += f"""
        <hr>
        <p style="color: red;">If you did not authorize this transaction, please <a href="{site_url}/support">contact support</a> immediately.</p>
        <p>Warm Regards,<br><strong style="color: #5F259F;">Mthree Banking</strong></p>
        </body>
        </html>
    """

    # Send HTML Email
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user_email]

    try:
        email = EmailMultiAlternatives(subject, html_message, from_email, recipient_list)
        email.attach_alternative(html_message, "text/html")  # Ensure it's sent as an HTML email
        email.send()
        print(f"HTML Email sent successfully for {transaction_type} to {user_email}")
    except Exception as e:
        print(f"Failed to send email: {str(e)}")

# def send_transaction_email(user_email,user_account_number,transaction_type,amount,user_balance,recipient_email=None, recipient_account_number=None,recipient_balance=0):
#     subject = f"{transaction_type} Confirmation"
#     print("_________Sending Mail to_________", user_email)
#     print("_________Transaction Type_________", transaction_type)
#     if transaction_type == "deposit":
#         messages = (
#             f"Dear Customer,\n\n"
#             f"Your deposit of Rs.{amount:.2f} into account **{user_account_number}** was successful. on {date.today()} at {datetime.now().strftime('%H:%M:%S')}\n"
#             f"Your updated account balance is Rs.{user_balance:.2f}.\n\n"
#             f"If you did not authorize this transaction, please contact support immediately.\n\n"
#             f"Warm Regards,\nMthree Banking"
#         )
#     elif transaction_type == "withdrawal":
#         messages = (
#             f"Dear Customer,\n\n"
#             f"Rs.{amount:.2f} has been withdrawn from your account **{user_account_number}** on {date.today()} at {datetime.now().strftime('%H:%M:%S')}.\n"
#             f"Your updated account balance is Rs.{user_balance:.2f}.\n\n"
#             f"If you did not authorize this transaction, please contact support immediately.\n\n"
#             f"Warm Regards,\nMthree Banking"
#         )
#     elif transaction_type == "transfer":
#         print("_________Transfer_________",user_account_number,recipient_account_number)
#         debit_messages = (
#             f"Dear Customer,\n\n"
#             f"Rs.{amount:.2f} has been debited from your account **{user_account_number}** to account **{recipient_account_number}** on {date.today()} at {datetime.now().strftime('%H:%M:%S')}.\n"
#             f"Your updated account balance is Rs.{user_balance:.2f}.\n\n"
#             f"If you did not authorize this transaction, please contact support immediately.\n\n"
#             f"Warm Regards,\nMthree Banking"
#         )
#         credit_messages = (
#             f"Dear Customer,\n\n"
#             f"Rs.{amount:.2f} has been credited to your account **{recipient_account_number}** from account **{user_account_number}** on {date.today()} at {datetime.now().strftime('%H:%M:%S')}.\n"
#             f"Your updated account balance is Rs.{recipient_balance:.2f}.\n\n"
#             f"If you did not authorize this transaction, please contact support immediately.\n\n"
#             f"Warm Regards,\nMthree Banking"
#         )
#         print("sending debit mail to user")
#         send_mail(subject, debit_messages, settings.EMAIL_HOST_USER, [user_email], fail_silently=False)  # debit mail to user
#         print(f"Email sent successfully for debit to {user_email}")
#         print("sending credit mail to recipient")
#         send_mail(subject, credit_messages, settings.EMAIL_HOST_USER, [recipient_email], fail_silently=False)  # credit mail to recipient
#         print(f"Email sent successfully for credit to {recipient_email}")
#         return 
#     print(transaction_type,"deposit",transaction_type == "deposit")
#     from_email = settings.EMAIL_HOST_USER
#     recipient_list = [user_email]
    
#     try:
#         send_mail(subject, messages, from_email, recipient_list, fail_silently=False)
#         print(f"Email sent successfully for {transaction_type} to {user_email}")
#     except Exception as e:
#         print(f"Failed to send email: {str(e)}")
#     return


#send email to user when they register


def send_registration_email(user_email, user_first_name):
    subject = "Welcome to Mthree Banking"
    site_url = "https://yourbank.com"  # Change this to your real domain
    banner_image_url = "https://i.imgur.com/PTL553r.png"  # Imgur banner image
    
    html_message = f"""
    <html>
    <body style="font-family: Arial, sans-serif; color: #333;">
        <center><img src="{banner_image_url}" width="100%" alt="Bank Banner"></center>
        <h2 style="color: #0275d8;">Welcome to Mthree Banking</h2>
        <p>Dear {user_first_name},</p>
        <p>Welcome to Mthree Banking! 🎉 We're thrilled to have you on board.</p>
        <p>Your account has been successfully registered, and you're now ready to experience secure and seamless banking. Here's what you can do next:</p>
        <ul>
            <li>✅ <strong>Explore Your Dashboard</strong> – Manage your finances effortlessly.</li>
            <li>✅ <strong>Set Up Security Features</strong> – Enhance your account protection.</li>
            <li>✅ <strong>Get Support Anytime</strong> – Our team is here for you 24/7.</li>
        </ul>
        <p>If you have any questions, feel free to reach out to our support team.</p>
        <hr>
        <p style="color: red;">If you did not authorize this registration, please <a href="{site_url}/support">contact support</a> immediately.</p>
        <p>Warm Regards,<br><strong style="color: #5F259F;">Mthree Banking Team</strong></p>
    </body>
    </html>
    """

    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user_email]
    
    try:
        email = EmailMultiAlternatives(subject, "", from_email, recipient_list)
        email.attach_alternative(html_message, "text/html")  # Ensure it's sent as an HTML email
        email.send()
        print(f"HTML Email sent successfully to {user_email}")
    except Exception as e:
        print(f"Failed to send email: {str(e)}")

"""
 account = get_object_or_404(Account, id=account_id)
    # Store account_id in session after login
    request.session['account_id'] = account.id  # Store the logged-in account ID
    request.session.modified = True  # Ensure session updates

"""