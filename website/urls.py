from django.urls import path
from . import views
from .views_entrance import entrance_page
from .views_courses import courses_page
from .views_courses import courses_page, university_fields, university_semesters
from .views_news import news_page

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
        path('courses/', courses_page, name='courses'),
        path('courses/university/<int:university_id>/', university_fields, name='university_fields'),
        path('courses/university/<int:university_id>/field/<str:field>/', university_semesters, name='university_semesters'),
    path('courses/semester/<int:semester>/', views.semester_detail, name='semester_detail'),
    path('courses/semester/<int:semester>/field/<str:field>/', views.field_detail, name='field_detail'),
    path('courses/semester/<int:semester>/field/<str:field>/university/<int:university_id>/', views.university_detail, name='university_detail'),
    path('courses/semester/<int:semester>/field/<str:field>/university/<int:university_id>/subject/<int:subject_id>/', views.subject_detail, name='subject_detail'),
    path('entrance/', entrance_page, name='entrance'),
    path('news/', news_page, name='news'),
]
