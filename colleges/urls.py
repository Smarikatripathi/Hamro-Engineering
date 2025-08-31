from django.urls import path
from . import views

app_name = 'colleges'

urlpatterns = [
    path('', views.CollegeListView.as_view(), name='college-list'),
    path('<int:id>/', views.CollegeDetailView.as_view(), name='college-detail'),
    path('programs/', views.EngineeringProgramListView.as_view(), name='program-list'),
    path('exams/', views.EntranceExamListView.as_view(), name='exam-list'),
    path('exams/<int:id>/', views.EntranceExamDetailView.as_view(), name='exam-detail'),
]
