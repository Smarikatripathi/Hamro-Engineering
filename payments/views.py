from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import timedelta

from .models import (
    SubscriptionPlan, UserSubscription, PaymentTransaction, 
    PaymentGateway, Refund
)
from .serializers import (
    SubscriptionPlanSerializer, UserSubscriptionSerializer,
    PaymentTransactionSerializer, PaymentGatewaySerializer, RefundSerializer
)


class SubscriptionPlanListView(generics.ListCreateAPIView):
    queryset = SubscriptionPlan.objects.filter(is_active=True)
    serializer_class = SubscriptionPlanSerializer
    permission_classes = [permissions.IsAuthenticated]


class SubscriptionPlanDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SubscriptionPlan.objects.all()
    serializer_class = SubscriptionPlanSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserSubscriptionListView(generics.ListAPIView):
    serializer_class = UserSubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return UserSubscription.objects.filter(user=self.request.user)


class UserSubscriptionDetailView(generics.RetrieveAPIView):
    serializer_class = UserSubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return UserSubscription.objects.filter(user=self.request.user)


class SubscribeView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, plan_id):
        plan = get_object_or_404(SubscriptionPlan, pk=plan_id, is_active=True)
        user = request.user
        
        # Check if user already has an active subscription
        active_subscription = UserSubscription.objects.filter(
            user=user,
            is_active=True
        ).first()
        
        if active_subscription:
            return Response({
                'message': 'You already have an active subscription'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Create subscription
        subscription = UserSubscription.objects.create(
            user=user,
            plan=plan,
            start_date=timezone.now(),
            end_date=timezone.now() + timedelta(days=plan.duration_days),
            is_active=True
        )
        
        return Response({
            'message': 'Subscription created successfully',
            'subscription_id': subscription.id
        }, status=status.HTTP_201_CREATED)


class PaymentTransactionListView(generics.ListAPIView):
    serializer_class = PaymentTransactionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return PaymentTransaction.objects.filter(user=self.request.user)


class PaymentTransactionDetailView(generics.RetrieveAPIView):
    serializer_class = PaymentTransactionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return PaymentTransaction.objects.filter(user=self.request.user)


class ProcessPaymentView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        # This would integrate with actual payment gateways
        # For now, just create a mock transaction
        transaction = PaymentTransaction.objects.create(
            user=request.user,
            amount=request.data.get('amount', 0),
            currency='NPR',
            payment_method=request.data.get('payment_method', 'khalti'),
            status='pending',
            gateway_reference=request.data.get('gateway_reference', ''),
            description=request.data.get('description', '')
        )
        
        return Response({
            'message': 'Payment processed successfully',
            'transaction_id': transaction.id
        }, status=status.HTTP_201_CREATED)


class PaymentGatewayListView(generics.ListAPIView):
    queryset = PaymentGateway.objects.filter(is_active=True)
    serializer_class = PaymentGatewaySerializer
    permission_classes = [permissions.IsAuthenticated]


class PaymentGatewayDetailView(generics.RetrieveAPIView):
    queryset = PaymentGateway.objects.all()
    serializer_class = PaymentGatewaySerializer
    permission_classes = [permissions.IsAuthenticated]


class RefundListView(generics.ListAPIView):
    serializer_class = RefundSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Refund.objects.filter(user=self.request.user)


class RefundDetailView(generics.RetrieveAPIView):
    serializer_class = RefundSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Refund.objects.filter(user=self.request.user)


class RequestRefundView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, transaction_id):
        transaction = get_object_or_404(
            PaymentTransaction, 
            pk=transaction_id, 
            user=request.user
        )
        
        if transaction.status != 'completed':
            return Response({
                'message': 'Only completed transactions can be refunded'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Create refund request
        refund = Refund.objects.create(
            user=request.user,
            transaction=transaction,
            amount=transaction.amount,
            reason=request.data.get('reason', ''),
            status='pending'
        )
        
        return Response({
            'message': 'Refund request submitted successfully',
            'refund_id': refund.id
        }, status=status.HTTP_201_CREATED)
