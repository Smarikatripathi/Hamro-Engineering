from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, StudentProfile, OTP, LoginAttempt


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'user_type', 'is_email_verified', 'is_staff', 'is_active', 'date_joined']
    list_filter = ['user_type', 'is_email_verified', 'is_staff', 'is_active', 'date_joined']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering = ['-date_joined']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Hamro Engineering', {'fields': ('user_type', 'phone_number', 'profile_picture', 'is_email_verified', 'email_verification_token')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Hamro Engineering', {'fields': ('user_type', 'phone_number', 'email')}),
    )


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'college', 'enrollment_year', 'total_mock_tests_taken', 'average_accuracy']
    list_filter = ['enrollment_year', 'college']
    search_fields = ['user__username', 'user__email', 'college__name']
    ordering = ['-created_at']


@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    list_display = ['user', 'otp_code', 'is_used', 'created_at', 'expires_at']
    list_filter = ['is_used', 'created_at']
    search_fields = ['user__username', 'user__email']
    ordering = ['-created_at']


@admin.register(LoginAttempt)
class LoginAttemptAdmin(admin.ModelAdmin):
    list_display = ['email', 'ip_address', 'timestamp', 'success']
    list_filter = ['success', 'timestamp']
    search_fields = ['email', 'ip_address']
    ordering = ['-timestamp']
