from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone

from .models import (
    Notification, Announcement, UserNotificationPreference, 
    Achievement, UserAchievement
)
from .serializers import (
    NotificationSerializer, AnnouncementSerializer, 
    UserNotificationPreferenceSerializer, AchievementSerializer, 
    UserAchievementSerializer
)


class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by('-created_at')


class NotificationDetailView(generics.RetrieveAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)


class MarkNotificationReadView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, pk):
        notification = get_object_or_404(
            Notification, 
            pk=pk, 
            user=request.user
        )
        
        notification.is_read = True
        notification.read_at = timezone.now()
        notification.save()
        
        return Response({
            'message': 'Notification marked as read'
        }, status=status.HTTP_200_OK)


class MarkAllNotificationsReadView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        Notification.objects.filter(
            user=request.user,
            is_read=False
        ).update(
            is_read=True,
            read_at=timezone.now()
        )
        
        return Response({
            'message': 'All notifications marked as read'
        }, status=status.HTTP_200_OK)


class AnnouncementListView(generics.ListAPIView):
    queryset = Announcement.objects.filter(is_published=True).order_by('-created_at')
    serializer_class = AnnouncementSerializer
    permission_classes = [permissions.IsAuthenticated]


class AnnouncementDetailView(generics.RetrieveAPIView):
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserNotificationPreferenceView(generics.RetrieveUpdateAPIView):
    serializer_class = UserNotificationPreferenceSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        obj, created = UserNotificationPreference.objects.get_or_create(
            user=self.request.user
        )
        return obj


class AchievementListView(generics.ListAPIView):
    queryset = Achievement.objects.filter(is_active=True)
    serializer_class = AchievementSerializer
    permission_classes = [permissions.IsAuthenticated]


class AchievementDetailView(generics.RetrieveAPIView):
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserAchievementListView(generics.ListAPIView):
    serializer_class = UserAchievementSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return UserAchievement.objects.filter(user=self.request.user)
