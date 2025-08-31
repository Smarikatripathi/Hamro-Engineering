from django.urls import path
from . import views

app_name = 'questions'

urlpatterns = [
    # Basic CRUD operations for questions
    path('', views.QuestionListView.as_view(), name='question-list'),
    path('<int:pk>/', views.QuestionDetailView.as_view(), name='question-detail'),
    
    # Mock test related URLs
    path('mock-tests/', views.MockTestListView.as_view(), name='mock-test-list'),
    path('mock-tests/<int:pk>/', views.MockTestDetailView.as_view(), name='mock-test-detail'),
    path('mock-tests/<int:pk>/start/', views.StartMockTestView.as_view(), name='start-mock-test'),
    path('mock-tests/<int:pk>/submit/', views.SubmitMockTestView.as_view(), name='submit-mock-test'),
    
    # Subject and topic URLs
    path('subjects/', views.SubjectListView.as_view(), name='subject-list'),
    path('subjects/<int:pk>/', views.SubjectDetailView.as_view(), name='subject-detail'),
    path('topics/', views.TopicListView.as_view(), name='topic-list'),
    path('topics/<int:pk>/', views.TopicDetailView.as_view(), name='topic-detail'),
    
    # Practice and bookmark URLs
    path('practice/<int:subject_id>/', views.PracticeView.as_view(), name='practice'),
    path('bookmark/<int:question_id>/', views.BookmarkQuestionView.as_view(), name='bookmark-question'),
    path('bookmarked/', views.BookmarkedQuestionsView.as_view(), name='bookmarked-questions'),
]
