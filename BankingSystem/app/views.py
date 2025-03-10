from django.shortcuts import render , redirect
from django.http import HttpResponse
# Create your views here.
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Account, Transaction
from .serializers import AccountSerializer, TransactionSerializer
from django.shortcuts import get_object_or_404
import decimal
from django.contrib import messages

@api_view(['POST'])
def deposit(request):
    account = get_object_or_404(Account, account_number=request.data.get('account_number'))
    amount = decimal.Decimal(request.data.get('amount', 0))
    
    if amount <= 0:
        return Response({'error': 'Invalid amount'}, status=status.HTTP_400_BAD_REQUEST)
    
    account.balance += amount
    account.save()
    
    Transaction.objects.create(
        account=account,
        transaction_type='deposit',
        amount=amount,
        balance_after=account.balance
    )
    
    return Response({'message': 'Deposit successful', 'balance': account.balance})

# Add more views for withdrawal, transfer, and interest credit  
def home(request):
    
    return render(request, 'home.html');

@api_view(['GET', 'POST'])
def register(request):
    if request.method == 'GET':
        print("GET request is accessed")
        return render(request, 'register.html')
    if request.method == 'POST':
        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            print("User registered successfully")
            #giveme code to alert to user that user is registered successfully
            messages.success(request, 'User registered successfully')
            return redirect('/')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return render(request, 'register.html')

@api_view(['GET', 'POST'])
def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    if request.method == 'POST':
        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return render(request, 'login.html')







