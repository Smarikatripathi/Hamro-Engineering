from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    # Notifications
    path('', views.NotificationListView.as_view(), name='notification-list'),
    path('<int:pk>/', views.NotificationDetailView.as_view(), name='notification-detail'),
    path('mark-read/<int:pk>/', views.MarkNotificationReadView.as_view(), name='mark-read'),
    path('mark-all-read/', views.MarkAllNotificationsReadView.as_view(), name='mark-all-read'),
    
    # Announcements
    path('announcements/', views.AnnouncementListView.as_view(), name='announcement-list'),
    path('announcements/<int:pk>/', views.AnnouncementDetailView.as_view(), name='announcement-detail'),
    
    # User preferences
    path('preferences/', views.UserNotificationPreferenceView.as_view(), name='preferences'),
    
    # Achievements
    path('achievements/', views.AchievementListView.as_view(), name='achievement-list'),
    path('achievements/<int:pk>/', views.AchievementDetailView.as_view(), name='achievement-detail'),
    path('user-achievements/', views.UserAchievementListView.as_view(), name='user-achievement-list'),
]
