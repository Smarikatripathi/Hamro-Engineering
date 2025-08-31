
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
import json

from notifications.models import Announcement
from questions.models import MockTest, Subject
from colleges.models import College
from payments.models import SubscriptionPlan, UserSubscription

# Payment unlock view
@login_required
@require_POST
@csrf_exempt
def pay_to_unlock(request):
    # Placeholder: In production, redirect to payment gateway (Khalti/eSewa/Fonepay)
    # For now, simulate payment success and activate subscription
    user = request.user
    # Get a default plan (e.g., first active plan)
    plan = SubscriptionPlan.objects.filter(is_active=True).first()
    if not plan:
        messages.error(request, 'No subscription plan available.')
        return redirect('website:pricing')
    # Create or activate subscription
    now = timezone.now()
    end_date = now + timedelta(days=30)  # Example: 30 days
    UserSubscription.objects.create(
        user=user,
        plan=plan,
        status='active',
        start_date=now,
        end_date=end_date
    )
    messages.success(request, 'Payment successful! Mock Test unlocked.')
    return redirect('website:mock_test')


def index(request):
    """Landing page view"""
    context = {
        'announcements': Announcement.objects.filter(is_published=True)[:5],
        'total_students': 1000,  # Mock data
        'total_questions': 5000,  # Mock data
        'total_colleges': 50,     # Mock data
    }
    return render(request, 'website/index.html', context)


def features(request):
    """Features page view"""
    return render(request, 'website/features.html')


def about(request):
    """About page view"""
    return render(request, 'website/about.html')


def contact(request):
    """Contact page view"""
    return render(request, 'website/contact.html')


@login_required
def dashboard(request):
    """Dashboard view for authenticated users"""
    user = request.user
    
    # Get user's active subscription - use status='active' instead of is_active
    active_subscription = None
    if hasattr(user, 'subscriptions'):
        active_subscription = user.subscriptions.filter(status='active').first()
    
    # Get available mock tests - use is_active field correctly
    available_tests = MockTest.objects.filter(is_active=True)[:5]
    
    # Get user's recent activity
    recent_activity = []
    if hasattr(user, 'mock_test_attempts'):
        recent_activity = user.mock_test_attempts.order_by('-created_at')[:5]
    
    context = {
        'user': user,
        'active_subscription': active_subscription,
        'available_tests': available_tests,
        'recent_activity': recent_activity,
    }
    return render(request, 'website/dashboard.html', context)


@csrf_exempt
def contact_form(request):
    """Handle contact form submissions"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name', '')
            email = data.get('email', '')
            subject = data.get('subject', '')
            message = data.get('message', '')
            
            # Validate required fields
            if not all([name, email, subject, message]):
                return JsonResponse({
                    'success': False,
                    'message': 'All fields are required'
                }, status=400)
            
            # Here you would typically save to database or send email
            # For now, just return success response
            
            return JsonResponse({
                'success': True,
                'message': 'Thank you for your message. We will get back to you soon!'
            })
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'message': 'Invalid data format'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': 'An error occurred. Please try again.'
            }, status=500)
    
    return JsonResponse({
        'success': False,
        'message': 'Method not allowed'
    }, status=405)


def pricing(request):
    """Pricing page view"""
    subscription_plans = SubscriptionPlan.objects.filter(is_active=True)
    context = {
        'plans': subscription_plans
    }
    return render(request, 'website/pricing.html', context)


def resources(request):
    """Resources page view"""
    subjects = Subject.objects.filter(is_active=True)
    colleges = College.objects.filter(is_active=True)[:10]
    
    context = {
        'subjects': subjects,
        'colleges': colleges,
    }
    return render(request, 'website/resources.html', context)


# MCQ Practice (Free)
def mcq_practice(request):
    return render(request, 'website/mcq_practice.html')

# Mock Test (Locked)
@login_required
def mock_test(request):
    user = request.user
    # Check if user has an active subscription
    active_subscription = UserSubscription.objects.filter(user=user, status='active').first()
    if not active_subscription:
        # Show locked message or redirect to pricing
        return render(request, 'website/mock_test_locked.html')
    # Show available mock tests
    available_tests = MockTest.objects.filter(is_active=True)
    return render(request, 'website/mock_test.html', {'available_tests': available_tests})
