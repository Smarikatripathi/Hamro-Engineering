from django.contrib import admin
from .models import Subject, Topic, Question, QuestionOption, MockTest, MockTestQuestion, MockTestAttempt, QuestionAttempt, BookmarkedQuestion


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['name']


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ['name', 'subject', 'description', 'is_active', 'created_at']
    list_filter = ['subject', 'is_active', 'created_at']
    search_fields = ['name', 'description', 'subject__name']
    ordering = ['subject__name', 'name']


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['question_text', 'topic', 'difficulty', 'question_type', 'is_active', 'created_at']
    list_filter = ['topic__subject', 'topic', 'difficulty', 'question_type', 'is_active', 'created_at']
    search_fields = ['question_text', 'explanation', 'topic__name', 'topic__subject__name']
    ordering = ['-created_at']


@admin.register(QuestionOption)
class QuestionOptionAdmin(admin.ModelAdmin):
    list_display = ['question', 'option_text', 'is_correct', 'order']
    list_filter = ['is_correct', 'order', 'question__topic__subject']
    search_fields = ['option_text', 'question__question_text']
    ordering = ['question', 'order']


@admin.register(MockTest)
class MockTestAdmin(admin.ModelAdmin):
    list_display = ['name', 'test_type', 'duration_minutes', 'total_questions', 'is_active', 'created_at']
    list_filter = ['test_type', 'is_active', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['-created_at']


@admin.register(MockTestQuestion)
class MockTestQuestionAdmin(admin.ModelAdmin):
    list_display = ['mock_test', 'question', 'order', 'marks']
    list_filter = ['mock_test__test_type', 'order']
    search_fields = ['mock_test__name', 'question__question_text']
    ordering = ['mock_test', 'order']


@admin.register(MockTestAttempt)
class MockTestAttemptAdmin(admin.ModelAdmin):
    list_display = ['user', 'mock_test', 'status', 'score', 'started_at', 'completed_at']
    list_filter = ['status', 'started_at', 'completed_at']
    search_fields = ['user__username', 'user__email', 'mock_test__name']
    ordering = ['-started_at']


@admin.register(QuestionAttempt)
class QuestionAttemptAdmin(admin.ModelAdmin):
    list_display = ['test_attempt', 'question', 'selected_option', 'is_correct', 'time_taken_seconds']
    list_filter = ['is_correct', 'answered_at']
    search_fields = ['question__question_text', 'test_attempt__user__username']
    ordering = ['-answered_at']


@admin.register(BookmarkedQuestion)
class BookmarkedQuestionAdmin(admin.ModelAdmin):
    list_display = ['user', 'question', 'created_at']
    list_filter = ['created_at', 'question__topic__subject']
    search_fields = ['user__username', 'question__question_text']
    ordering = ['-created_at']
