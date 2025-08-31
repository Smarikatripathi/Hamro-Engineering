
from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    # User-facing notifications page
    path('', views.notifications_page, name='notifications-page'),

    # API endpoints
    path('api/', views.NotificationListView.as_view(), name='notification-list'),
    path('api/<int:pk>/', views.NotificationDetailView.as_view(), name='notification-detail'),
    path('api/mark-read/<int:pk>/', views.MarkNotificationReadView.as_view(), name='mark-read'),
    path('api/mark-all-read/', views.MarkAllNotificationsReadView.as_view(), name='mark-all-read'),

    # Announcements
    path('api/announcements/', views.AnnouncementListView.as_view(), name='announcement-list'),
    path('api/announcements/<int:pk>/', views.AnnouncementDetailView.as_view(), name='announcement-detail'),

    # User preferences
    path('api/preferences/', views.UserNotificationPreferenceView.as_view(), name='preferences'),

    # Achievements
    path('api/achievements/', views.AchievementListView.as_view(), name='achievement-list'),
    path('api/achievements/<int:pk>/', views.AchievementDetailView.as_view(), name='achievement-detail'),
    path('api/user-achievements/', views.UserAchievementListView.as_view(), name='user-achievement-list'),
]
