from django.contrib import admin
from .models import SubscriptionPlan, UserSubscription, PaymentTransaction, PaymentGateway, Refund


@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'plan_type', 'duration', 'price', 'is_active', 'created_at']
    list_filter = ['plan_type', 'duration', 'is_active', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['price']


@admin.register(UserSubscription)
class UserSubscriptionAdmin(admin.ModelAdmin):
    list_display = ['user', 'plan', 'status', 'start_date', 'end_date', 'auto_renew', 'created_at']
    list_filter = ['status', 'auto_renew', 'start_date', 'end_date', 'created_at']
    search_fields = ['user__username', 'user__email', 'plan__name']
    ordering = ['-created_at']


@admin.register(PaymentTransaction)
class PaymentTransactionAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount', 'payment_method', 'status', 'transaction_id', 'created_at']
    list_filter = ['payment_method', 'status', 'created_at']
    search_fields = ['user__username', 'transaction_id', 'gateway_transaction_id']
    ordering = ['-created_at']


@admin.register(PaymentGateway)
class PaymentGatewayAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'test_mode', 'created_at']
    list_filter = ['is_active', 'test_mode', 'created_at']
    search_fields = ['name', 'merchant_id']
    ordering = ['name']


@admin.register(Refund)
class RefundAdmin(admin.ModelAdmin):
    list_display = ['payment', 'amount', 'reason', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['payment__transaction_id', 'reason']
    ordering = ['-created_at']
