from django.contrib import admin
from .models import Notification, Announcement, UserNotificationPreference, Achievement, UserAchievement


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['recipient', 'title', 'notification_type', 'is_read', 'created_at']
    list_filter = ['notification_type', 'is_read', 'created_at']
    search_fields = ['recipient__username', 'title', 'message']
    ordering = ['-created_at']


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ['title', 'announcement_type', 'is_published', 'published_at', 'expires_at', 'created_by', 'created_at']
    list_filter = ['announcement_type', 'is_published', 'published_at', 'expires_at', 'created_at']
    search_fields = ['title', 'content', 'created_by__username']
    ordering = ['-created_at']


@admin.register(UserNotificationPreference)
class UserNotificationPreferenceAdmin(admin.ModelAdmin):
    list_display = ['user', 'email_notifications', 'push_notifications', 'daily_digest', 'created_at']
    list_filter = ['email_notifications', 'push_notifications', 'daily_digest', 'created_at']
    search_fields = ['user__username', 'user__email']
    ordering = ['-created_at']


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'points', 'is_active', 'created_at']
    list_filter = ['is_active', 'points', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['name']


@admin.register(UserAchievement)
class UserAchievementAdmin(admin.ModelAdmin):
    list_display = ['user', 'achievement', 'unlocked_at']
    list_filter = ['unlocked_at', 'achievement__is_active']
    search_fields = ['user__username', 'achievement__name']
    ordering = ['-unlocked_at']
