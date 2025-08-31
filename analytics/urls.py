from django.urls import path
from . import views

app_name = 'analytics'

urlpatterns = [
    path('student/', views.StudentAnalyticsView.as_view(), name='student-analytics'),
    path('admin/', views.AdminAnalyticsView.as_view(), name='admin-analytics'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('subject/<int:subject_id>/', views.subject_analytics, name='subject-analytics'),
]
