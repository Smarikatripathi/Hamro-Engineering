from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # API endpoints only
    path('register/', views.UserRegistrationView.as_view(), name='api-register'),
    path('login/', views.UserLoginView.as_view(), name='api-login'),
    path('logout/', views.UserLogoutView.as_view(), name='api-logout'),
    path('verify-otp/', views.OTPVerificationView.as_view(), name='api-verify-otp'),
    
    # Password management
    path('password-reset/', views.PasswordResetView.as_view(), name='api-password-reset'),
    path('password-change/', views.PasswordChangeView.as_view(), name='api-password-change'),
    
    # Profile management
    path('profile/', views.ProfileView.as_view(), name='api-profile'),
    path('profile/update/', views.ProfileUpdateView.as_view(), name='api-profile-update'),
    path('student-profile/', views.StudentProfileView.as_view(), name='api-student-profile'),
    
    # User management
    path('users/', views.UserListView.as_view(), name='api-user-list'),
    path('users/<int:pk>/', views.UserDetailView.as_view(), name='api-user-detail'),
]
