from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    # Subscription plans
    path('plans/', views.SubscriptionPlanListView.as_view(), name='plan-list'),
    path('plans/<int:pk>/', views.SubscriptionPlanDetailView.as_view(), name='plan-detail'),
    
    # User subscriptions
    path('subscriptions/', views.UserSubscriptionListView.as_view(), name='subscription-list'),
    path('subscriptions/<int:pk>/', views.UserSubscriptionDetailView.as_view(), name='subscription-detail'),
    path('subscribe/<int:plan_id>/', views.SubscribeView.as_view(), name='subscribe'),
    
    # Payment transactions
    path('transactions/', views.PaymentTransactionListView.as_view(), name='transaction-list'),
    path('transactions/<int:pk>/', views.PaymentTransactionDetailView.as_view(), name='transaction-detail'),
    path('process-payment/', views.ProcessPaymentView.as_view(), name='process-payment'),
    
    # Payment gateways
    path('gateways/', views.PaymentGatewayListView.as_view(), name='gateway-list'),
    path('gateways/<int:pk>/', views.PaymentGatewayDetailView.as_view(), name='gateway-detail'),
    
    # Refunds
    path('refunds/', views.RefundListView.as_view(), name='refund-list'),
    path('refunds/<int:pk>/', views.RefundDetailView.as_view(), name='refund-detail'),
    path('request-refund/<int:transaction_id>/', views.RequestRefundView.as_view(), name='request-refund'),
]
