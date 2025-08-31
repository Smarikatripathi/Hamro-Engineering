from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import User, StudentProfile, OTP, LoginAttempt
from colleges.models import College, EngineeringProgram, EntranceExam
from questions.models import Subject, Topic, Question, QuestionOption, MockTest, MockTestQuestion, MockTestAttempt, QuestionAttempt, BookmarkedQuestion
from payments.models import SubscriptionPlan, UserSubscription, PaymentTransaction, PaymentGateway, Refund
from notifications.models import Notification, Announcement, UserNotificationPreference, Achievement, UserAchievement


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['email', 'username', 'first_name', 'last_name', 'user_type', 'is_email_verified', 'is_active', 'date_joined']
    list_filter = ['user_type', 'is_email_verified', 'is_active', 'date_joined']
    search_fields = ['email', 'username', 'first_name', 'last_name']
    ordering = ['-date_joined']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('user_type', 'phone_number', 'profile_picture', 'is_email_verified', 'email_verification_token')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('user_type', 'phone_number')}),
    )


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'college', 'enrollment_year', 'total_mock_tests_taken', 'average_accuracy']
    list_filter = ['college', 'enrollment_year']
    search_fields = ['user__username', 'user__email', 'college__name']


@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    list_display = ['user', 'otp_code', 'is_used', 'created_at', 'expires_at']
    list_filter = ['is_used', 'created_at']
    search_fields = ['user__email']


@admin.register(LoginAttempt)
class LoginAttemptAdmin(admin.ModelAdmin):
    list_display = ['email', 'ip_address', 'timestamp', 'success']
    list_filter = ['success', 'timestamp']
    search_fields = ['email']


@admin.register(College)
class CollegeAdmin(admin.ModelAdmin):
    list_display = ['name', 'university', 'location', 'established_year', 'is_active']
    list_filter = ['university', 'is_active', 'established_year']
    search_fields = ['name', 'location']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(EngineeringProgram)
class EngineeringProgramAdmin(admin.ModelAdmin):
    list_display = ['name', 'college', 'program_type', 'duration_years', 'total_seats', 'available_seats']
    list_filter = ['program_type', 'duration_years', 'is_active']
    search_fields = ['name', 'college__name']


@admin.register(EntranceExam)
class EntranceExamAdmin(admin.ModelAdmin):
    list_display = ['name', 'exam_type', 'college', 'exam_date', 'registration_deadline', 'is_active']
    list_filter = ['exam_type', 'is_active', 'exam_date']
    search_fields = ['name', 'college__name']


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name']


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ['name', 'subject', 'difficulty_level', 'is_active']
    list_filter = ['subject', 'difficulty_level', 'is_active']
    search_fields = ['name', 'subject__name']


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['topic', 'question_type', 'difficulty', 'marks', 'is_active']
    list_filter = ['topic__subject', 'question_type', 'difficulty', 'is_active']
    search_fields = ['question_text', 'topic__name']
    list_per_page = 20


@admin.register(QuestionOption)
class QuestionOptionAdmin(admin.ModelAdmin):
    list_display = ['question', 'option_text', 'is_correct', 'order']
    list_filter = ['is_correct', 'question__topic__subject']
    search_fields = ['option_text', 'question__question_text']


@admin.register(MockTest)
class MockTestAdmin(admin.ModelAdmin):
    list_display = ['name', 'test_type', 'duration_minutes', 'total_questions', 'is_free', 'price', 'is_active']
    list_filter = ['test_type', 'is_free', 'is_active', 'created_at']
    search_fields = ['name', 'description']


@admin.register(MockTestQuestion)
class MockTestQuestionAdmin(admin.ModelAdmin):
    list_display = ['mock_test', 'question', 'order', 'marks']
    list_filter = ['mock_test__test_type', 'question__topic__subject']
    search_fields = ['mock_test__name', 'question__question_text']


@admin.register(MockTestAttempt)
class MockTestAttemptAdmin(admin.ModelAdmin):
    list_display = ['user', 'mock_test', 'status', 'score', 'accuracy_percentage', 'started_at']
    list_filter = ['status', 'mock_test__test_type', 'started_at']
    search_fields = ['user__username', 'user__email', 'mock_test__name']
    readonly_fields = ['started_at', 'completed_at']


@admin.register(QuestionAttempt)
class QuestionAttemptAdmin(admin.ModelAdmin):
    list_display = ['test_attempt', 'question', 'is_correct', 'time_taken_seconds', 'is_marked_for_review']
    list_filter = ['is_correct', 'is_marked_for_review', 'question__topic__subject']
    search_fields = ['test_attempt__user__username', 'question__question_text']


@admin.register(BookmarkedQuestion)
class BookmarkedQuestionAdmin(admin.ModelAdmin):
    list_display = ['user', 'question', 'created_at']
    list_filter = ['created_at', 'question__topic__subject']
    search_fields = ['user__username', 'question__question_text']


@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'plan_type', 'duration', 'price', 'is_active']
    list_filter = ['plan_type', 'duration', 'is_active']
    search_fields = ['name', 'description']


@admin.register(UserSubscription)
class UserSubscriptionAdmin(admin.ModelAdmin):
    list_display = ['user', 'plan', 'status', 'start_date', 'end_date', 'auto_renew']
    list_filter = ['status', 'plan__plan_type', 'auto_renew']
    search_fields = ['user__username', 'user__email', 'plan__name']


@admin.register(PaymentTransaction)
class PaymentTransactionAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount', 'payment_method', 'transaction_id', 'status', 'created_at']
    list_filter = ['payment_method', 'status', 'created_at']
    search_fields = ['user__username', 'user__email', 'transaction_id']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(PaymentGateway)
class PaymentGatewayAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'test_mode', 'created_at']
    list_filter = ['is_active', 'test_mode']
    search_fields = ['name']


@admin.register(Refund)
class RefundAdmin(admin.ModelAdmin):
    list_display = ['payment', 'amount', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['payment__transaction_id']


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['recipient', 'notification_type', 'title', 'priority', 'is_read', 'created_at']
    list_filter = ['notification_type', 'priority', 'is_read', 'created_at']
    search_fields = ['recipient__username', 'title', 'message']
    list_per_page = 50


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ['title', 'announcement_type', 'is_published', 'published_at', 'created_by', 'created_at']
    list_filter = ['announcement_type', 'is_published', 'created_at']
    search_fields = ['title', 'content']
    actions = ['publish_announcements']
    
    def publish_announcements(self, request, queryset):
        for announcement in queryset:
            announcement.publish()
        self.message_user(request, f"{queryset.count()} announcements published successfully.")
    publish_announcements.short_description = "Publish selected announcements"


@admin.register(UserNotificationPreference)
class UserNotificationPreferenceAdmin(admin.ModelAdmin):
    list_display = ['user', 'email_notifications', 'push_notifications', 'daily_digest', 'weekly_summary']
    list_filter = ['email_notifications', 'push_notifications', 'daily_digest', 'weekly_summary']
    search_fields = ['user__username', 'user__email']


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ['name', 'achievement_type', 'points', 'is_active']
    list_filter = ['achievement_type', 'is_active']
    search_fields = ['name', 'description']


@admin.register(UserAchievement)
class UserAchievementAdmin(admin.ModelAdmin):
    list_display = ['user', 'achievement', 'unlocked_at']
    list_filter = ['achievement__achievement_type', 'unlocked_at']
    search_fields = ['user__username', 'achievement__name']


# Customize admin site
admin.site.site_header = "Hamro Engineering Administration"
admin.site.site_title = "Hamro Engineering Admin"
admin.site.index_title = "Welcome to Hamro Engineering Admin Portal"
