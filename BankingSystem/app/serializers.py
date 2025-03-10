from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Account, Transaction

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ( 'email', 'password', 'firstname', 'lastname')
        extra_kwargs = {'password': {'write_only': True}}

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'