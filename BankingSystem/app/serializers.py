from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Account, Transaction, Customer , AccountType, TransferIn, TransferOut,Address

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ( 'username', 'email', 'password', 'first_name', 'last_name')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            username=validated_data['first_name']+validated_data['last_name'],  # Use email as username
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])  # Hash the password
        user.save()
        return user
# class CustomerSerializer(serializers.ModelSerializer):
#     user = UserSerializer()
#     class Meta:
#         model = Customer
#         fields = '__all__'

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields='__all__'
        extra_kwargs = {
            # 'user': {'read_only': True},  # Prevent user from being changed via API
            'employee': {'required': False}  # Make employee optional if needed
        }
class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'customer', 'street', 'city', 'state', 'zip_code', 'country']
 
class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}



class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'