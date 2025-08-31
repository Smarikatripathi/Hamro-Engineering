from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Count, Avg, Sum, Q
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model

from questions.models import MockTestAttempt, QuestionAttempt, Subject, Topic
from payments.models import PaymentTransaction, UserSubscription
from accounts.models import StudentProfile

User = get_user_model()


class StudentAnalyticsView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        user = request.user
        student_profile = getattr(user, 'student_profile', None)
        
        if not student_profile:
            return Response({'error': 'Student profile not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Get test attempts
        test_attempts = MockTestAttempt.objects.filter(user=user)
        completed_tests = test_attempts.filter(status='completed')
        
        # Calculate statistics
        total_tests_taken = completed_tests.count()
        average_score = completed_tests.aggregate(avg_score=Avg('score'))['avg_score'] or 0
        average_accuracy = completed_tests.aggregate(avg_accuracy=Avg('accuracy_percentage'))['avg_accuracy'] or 0
        total_study_time = completed_tests.aggregate(total_time=Sum('time_taken_minutes'))['total_time'] or 0
        
        # Subject-wise performance
        subject_performance = []
        subjects = Subject.objects.all()
        
        for subject in subjects:
            subject_questions = QuestionAttempt.objects.filter(
                test_attempt__user=user,
                question__topic__subject=subject
            )
            
            if subject_questions.exists():
                correct_answers = subject_questions.filter(is_correct=True).count()
                total_questions = subject_questions.count()
                accuracy = (correct_answers / total_questions) * 100 if total_questions > 0 else 0
                
                subject_performance.append({
                    'subject': subject.name,
                    'total_questions': total_questions,
                    'correct_answers': correct_answers,
                    'accuracy': round(accuracy, 2)
                })
        
        # Recent activity
        recent_attempts = completed_tests.order_by('-completed_at')[:5]
        recent_activity = []
        
        for attempt in recent_attempts:
            recent_activity.append({
                'test_name': attempt.mock_test.name,
                'score': float(attempt.score),
                'accuracy': float(attempt.accuracy_percentage),
                'completed_at': attempt.completed_at
            })
        
        # Progress over time (last 30 days)
        thirty_days_ago = timezone.now() - timedelta(days=30)
        daily_progress = []
        
        for i in range(30):
            date = thirty_days_ago + timedelta(days=i)
            day_start = date.replace(hour=0, minute=0, second=0, microsecond=0)
            day_end = day_start + timedelta(days=1)
            
            day_tests = completed_tests.filter(completed_at__gte=day_start, completed_at__lt=day_end)
            day_score = day_tests.aggregate(avg_score=Avg('score'))['avg_score'] or 0
            
            daily_progress.append({
                'date': date.strftime('%Y-%m-%d'),
                'score': float(day_score),
                'tests_taken': day_tests.count()
            })
        
        analytics_data = {
            'overview': {
                'total_tests_taken': total_tests_taken,
                'average_score': float(average_score),
                'average_accuracy': float(average_accuracy),
                'total_study_time_minutes': total_study_time
            },
            'subject_performance': subject_performance,
            'recent_activity': recent_activity,
            'daily_progress': daily_progress
        }
        
        return Response(analytics_data)


class AdminAnalyticsView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        # Check if user is admin
        if request.user.user_type != 'admin':
            return Response({'error': 'Admin access required'}, status=status.HTTP_403_FORBIDDEN)
        
        # User statistics
        total_users = User.objects.filter(user_type='student').count()
        active_users = User.objects.filter(
            user_type='student',
            last_login__gte=timezone.now() - timedelta(days=30)
        ).count()
        
        # Test statistics
        total_test_attempts = MockTestAttempt.objects.count()
        completed_tests = MockTestAttempt.objects.filter(status='completed').count()
        average_test_score = MockTestAttempt.objects.filter(status='completed').aggregate(
            avg_score=Avg('score')
        )['avg_score'] or 0
        
        # Payment statistics
        total_revenue = PaymentTransaction.objects.filter(status='completed').aggregate(
            total=Sum('amount')
        )['total'] or 0
        
        active_subscriptions = UserSubscription.objects.filter(status='active').count()
        
        # Subject popularity
        subject_stats = Subject.objects.annotate(
            question_count=Count('topics__questions'),
            test_count=Count('topics__questions__mocktestquestion__mock_test', distinct=True)
        ).values('name', 'question_count', 'test_count')
        
        # Recent registrations
        recent_users = User.objects.filter(
            user_type='student',
            date_joined__gte=timezone.now() - timedelta(days=7)
        ).count()
        
        analytics_data = {
            'user_statistics': {
                'total_users': total_users,
                'active_users': active_users,
                'recent_registrations': recent_users
            },
            'test_statistics': {
                'total_attempts': total_test_attempts,
                'completed_tests': completed_tests,
                'average_score': float(average_test_score)
            },
            'financial_statistics': {
                'total_revenue': float(total_revenue),
                'active_subscriptions': active_subscriptions
            },
            'subject_statistics': list(subject_stats)
        }
        
        return Response(analytics_data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def leaderboard(request):
    """Get leaderboard data"""
    timeframe = request.GET.get('timeframe', 'all')  # all, week, month
    
    if timeframe == 'week':
        start_date = timezone.now() - timedelta(days=7)
        attempts = MockTestAttempt.objects.filter(
            status='completed',
            completed_at__gte=start_date
        )
    elif timeframe == 'month':
        start_date = timezone.now() - timedelta(days=30)
        attempts = MockTestAttempt.objects.filter(
            status='completed',
            completed_at__gte=start_date
        )
    else:
        attempts = MockTestAttempt.objects.filter(status='completed')
    
    # Get top performers
    leaderboard_data = attempts.values(
        'user__username',
        'user__first_name',
        'user__last_name'
    ).annotate(
        total_tests=Count('id'),
        average_score=Avg('score'),
        best_score=Avg('score'),
        total_time=Sum('time_taken_minutes')
    ).order_by('-average_score', '-total_tests')[:20]
    
    # Format data
    formatted_leaderboard = []
    for i, entry in enumerate(leaderboard_data, 1):
        formatted_leaderboard.append({
            'rank': i,
            'username': entry['user__username'],
            'full_name': f"{entry['user__first_name']} {entry['user__last_name']}",
            'total_tests': entry['total_tests'],
            'average_score': round(float(entry['average_score']), 2),
            'best_score': round(float(entry['best_score']), 2),
            'total_time_minutes': entry['total_time'] or 0
        })
    
    return Response({
        'timeframe': timeframe,
        'leaderboard': formatted_leaderboard
    })


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def subject_analytics(request, subject_id):
    """Get detailed analytics for a specific subject"""
    try:
        subject = Subject.objects.get(id=subject_id)
    except Subject.DoesNotExist:
        return Response({'error': 'Subject not found'}, status=status.HTTP_404_NOT_FOUND)
    
    user = request.user
    
    # Get user's performance in this subject
    subject_questions = QuestionAttempt.objects.filter(
        test_attempt__user=user,
        question__topic__subject=subject
    )
    
    if not subject_questions.exists():
        return Response({'error': 'No data available for this subject'}, status=status.HTTP_404_NOT_FOUND)
    
    # Calculate statistics
    total_questions = subject_questions.count()
    correct_answers = subject_questions.filter(is_correct=True).count()
    accuracy = (correct_answers / total_questions) * 100
    
    # Topic-wise breakdown
    topic_performance = []
    topics = Topic.objects.filter(subject=subject)
    
    for topic in topics:
        topic_questions = subject_questions.filter(question__topic=topic)
        if topic_questions.exists():
            topic_correct = topic_questions.filter(is_correct=True).count()
            topic_total = topic_questions.count()
            topic_accuracy = (topic_correct / topic_total) * 100
            
            topic_performance.append({
                'topic_name': topic.name,
                'total_questions': topic_total,
                'correct_answers': topic_correct,
                'accuracy': round(topic_accuracy, 2),
                'difficulty': topic.difficulty_level
            })
    
    # Time analysis
    avg_time_per_question = subject_questions.aggregate(
        avg_time=Avg('time_taken_seconds')
    )['avg_time'] or 0
    
    analytics_data = {
        'subject': subject.name,
        'overview': {
            'total_questions': total_questions,
            'correct_answers': correct_answers,
            'accuracy': round(accuracy, 2),
            'average_time_per_question_seconds': round(avg_time_per_question, 2)
        },
        'topic_breakdown': topic_performance
    }
    
    return Response(analytics_data)
