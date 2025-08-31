from django.urls import path
from . import views

app_name = 'website'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('features/', views.features, name='features'),
    path('contact/', views.contact, name='contact'),
    path('pricing/', views.pricing, name='pricing'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('contact-form/', views.contact_form, name='contact_form'),
    path('mcq-practice/', views.mcq_practice, name='mcq_practice'),
    path('mock-test/', views.mock_test, name='mock_test'),
    path('pay-to-unlock/', views.pay_to_unlock, name='pay_to_unlock'),
    path('resources/', views.resources, name='resources'),
]
