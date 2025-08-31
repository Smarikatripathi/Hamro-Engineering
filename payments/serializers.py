from rest_framework import serializers
from .models import (
    SubscriptionPlan, UserSubscription, PaymentTransaction, 
    PaymentGateway, Refund
)


class SubscriptionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPlan
        fields = [
            'id', 'name', 'description', 'price', 'currency',
            'duration_days', 'features', 'is_active', 'created_at'
        ]


class UserSubscriptionSerializer(serializers.ModelSerializer):
    plan = SubscriptionPlanSerializer(read_only=True)
    
    class Meta:
        model = UserSubscription
        fields = [
            'id', 'user', 'plan', 'start_date', 'end_date',
            'is_active', 'created_at', 'updated_at'
        ]


class PaymentGatewaySerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentGateway
        fields = [
            'id', 'name', 'gateway_type', 'is_active',
            'config_data', 'created_at'
        ]


class PaymentTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentTransaction
        fields = [
            'id', 'user', 'amount', 'currency', 'payment_method',
            'status', 'gateway_reference', 'description',
            'created_at', 'updated_at'
        ]


class RefundSerializer(serializers.ModelSerializer):
    transaction = PaymentTransactionSerializer(read_only=True)
    
    class Meta:
        model = Refund
        fields = [
            'id', 'user', 'transaction', 'amount', 'reason',
            'status', 'processed_at', 'created_at'
        ]
