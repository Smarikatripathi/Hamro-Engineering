from rest_framework import serializers
from .models import (
    Notification, Announcement, UserNotificationPreference, 
    Achievement, UserAchievement
)


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = [
            'id', 'user', 'title', 'message', 'notification_type',
            'is_read', 'read_at', 'created_at'
        ]


class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = [
            'id', 'title', 'content', 'announcement_type',
            'is_published', 'published_at', 'expires_at', 'created_by',
            'created_at', 'updated_at'
        ]


class UserNotificationPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserNotificationPreference
        fields = [
            'id', 'user', 'email_notifications', 'push_notifications',
            'sms_notifications', 'created_at', 'updated_at'
        ]


class AchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achievement
        fields = [
            'id', 'name', 'description', 'icon', 'points',
            'is_active', 'created_at'
        ]


class UserAchievementSerializer(serializers.ModelSerializer):
    achievement = AchievementSerializer(read_only=True)
    
    class Meta:
        model = UserAchievement
        fields = [
            'id', 'user', 'achievement', 'earned_at', 'created_at'
        ]
