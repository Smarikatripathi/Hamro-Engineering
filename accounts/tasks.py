from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string


@shared_task
def send_otp_email(email, otp_code):
    """Send OTP verification email to user"""
    subject = 'Email Verification - Hamro Engineering'
    
    # Simple email content
    message = f"""
    Hello!
    
    Your verification code is: {otp_code}
    
    This code will expire in 10 minutes.
    
    If you didn't request this code, please ignore this email.
    
    Best regards,
    Hamro Engineering Team
    """
    
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False,
        )
        return f"OTP email sent successfully to {email}"
    except Exception as e:
        return f"Failed to send OTP email to {email}: {str(e)}"


@shared_task
def send_welcome_email(email, username):
    """
    Send welcome email after successful registration
    """
    subject = 'Welcome to Hamro Engineering!'
    
    html_message = render_to_string('accounts/email/welcome.html', {
        'username': username,
        'company_name': 'Hamro Engineering'
    })
    
    message = f"""
    Welcome {username} to Hamro Engineering!
    
    Your account has been successfully created and verified.
    
    Start your engineering preparation journey with us!
    
    Best regards,
    Hamro Engineering Team
    """
    
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            html_message=html_message,
            fail_silently=False,
        )
        return f"Welcome email sent successfully to {email}"
    except Exception as e:
        return f"Failed to send welcome email to {email}: {str(e)}"


@shared_task
def send_password_reset_email(email, otp_code):
    """Send password reset OTP email to user"""
    subject = 'Password Reset - Hamro Engineering'
    
    message = f"""
    Hello!
    
    You requested a password reset. Your reset code is: {otp_code}
    
    This code will expire in 10 minutes.
    
    If you didn't request this reset, please ignore this email.
    
    Best regards,
    Hamro Engineering Team
    """
    
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False,
        )
        return f"Password reset email sent successfully to {email}"
    except Exception as e:
        return f"Failed to send password reset email to {email}: {str(e)}"
