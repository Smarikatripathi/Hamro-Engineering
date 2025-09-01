
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from accounts import views as accounts_views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Template views (user-facing pages)
    path('accounts/register/', accounts_views.register_page, name='register'),
    path('accounts/login/', accounts_views.login_page, name='login'),
    path('accounts/logout/', accounts_views.logout_view, name='logout'),
    
    # API endpoints
    path('api/accounts/', include('accounts.urls')),
    path('api/colleges/', include('colleges.urls')),
    path('api/questions/', include('questions.urls')),
    path('api/payments/', include('payments.urls')),
    path('api/analytics/', include('analytics.urls')),
    path('notifications/', include('notifications.urls')),
    path('resources/', include('resources.urls')),
    path('', include('website.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
