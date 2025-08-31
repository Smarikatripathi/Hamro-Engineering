from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

User = get_user_model()


class Notification(models.Model):
    NOTIFICATION_TYPE_CHOICES = [
        ('test_result', 'Test Result'),
        ('new_test', 'New Test Available'),
        ('payment_success', 'Payment Successful'),
        ('payment_failed', 'Payment Failed'),
        ('subscription_expiry', 'Subscription Expiring'),
        ('announcement', 'Announcement'),
        ('achievement', 'Achievement Unlocked'),
        ('reminder', 'Reminder'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPE_CHOICES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    is_read = models.BooleanField(default=False)
    is_sent = models.BooleanField(default=False)
    
    # Generic foreign key for related object
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    
    # Additional data
    data = models.JSONField(default=dict, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.recipient.username} - {self.title}"
    
    def mark_as_read(self):
        from django.utils import timezone
        self.is_read = True
        self.read_at = timezone.now()
        self.save()


class Announcement(models.Model):
    ANNOUNCEMENT_TYPE_CHOICES = [
        ('general', 'General'),
        ('academic', 'Academic'),
        ('technical', 'Technical'),
        ('maintenance', 'Maintenance'),
        ('update', 'System Update'),
    ]
    
    title = models.CharField(max_length=200)
    content = models.TextField()
    announcement_type = models.CharField(max_length=15, choices=ANNOUNCEMENT_TYPE_CHOICES, default='general')
    is_published = models.BooleanField(default=False)
    published_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-published_at', '-created_at']
    
    def __str__(self):
        return self.title
    
    def publish(self):
        from django.utils import timezone
        self.is_published = True
        self.published_at = timezone.now()
        self.save()
        
        # Create notifications for all users
        users = User.objects.filter(user_type='student', is_active=True)
        notifications = []
        
        for user in users:
            notification = Notification(
                recipient=user,
                notification_type='announcement',
                title=self.title,
                message=self.content[:100] + '...' if len(self.content) > 100 else self.content,
                priority='medium',
                content_object=self
            )
            notifications.append(notification)
        
        if notifications:
            Notification.objects.bulk_create(notifications)


class UserNotificationPreference(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='notification_preferences')
    
    # Email preferences
    email_notifications = models.BooleanField(default=True)
    email_test_results = models.BooleanField(default=True)
    email_payments = models.BooleanField(default=True)
    email_announcements = models.BooleanField(default=True)
    email_achievements = models.BooleanField(default=True)
    email_reminders = models.BooleanField(default=True)
    
    # Push notification preferences
    push_notifications = models.BooleanField(default=True)
    push_test_results = models.BooleanField(default=True)
    push_payments = models.BooleanField(default=True)
    push_announcements = models.BooleanField(default=True)
    push_achievements = models.BooleanField(default=True)
    push_reminders = models.BooleanField(default=True)
    
    # Frequency preferences
    daily_digest = models.BooleanField(default=False)
    weekly_summary = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Notification preferences for {self.user.username}"


class Achievement(models.Model):
    ACHIEVEMENT_TYPE_CHOICES = [
        ('test_score', 'Test Score'),
        ('test_count', 'Test Count'),
        ('streak', 'Streak'),
        ('accuracy', 'Accuracy'),
        ('time_spent', 'Time Spent'),
        ('subject_mastery', 'Subject Mastery'),
    ]
    
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    achievement_type = models.CharField(max_length=20, choices=ACHIEVEMENT_TYPE_CHOICES)
    icon = models.CharField(max_length=50, blank=True, null=True)  # For FontAwesome icons
    criteria = models.JSONField(default=dict)  # Store achievement criteria
    points = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['points', 'name']
    
    def __str__(self):
        return self.name


class UserAchievement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='achievements')
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    unlocked_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'achievement']
        ordering = ['-unlocked_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.achievement.name}"
