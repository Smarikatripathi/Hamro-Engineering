from rest_framework import serializers
from .models import (
    Question, QuestionOption, Subject, Topic, MockTest, MockTestQuestion,
    MockTestAttempt, QuestionAttempt, BookmarkedQuestion
)


class QuestionOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionOption
        fields = ['id', 'option_text', 'is_correct']


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'name', 'description', 'is_active']


class TopicSerializer(serializers.ModelSerializer):
    subject = SubjectSerializer(read_only=True)
    
    class Meta:
        model = Topic
        fields = ['id', 'name', 'description', 'subject', 'is_active']


class QuestionSerializer(serializers.ModelSerializer):
    options = QuestionOptionSerializer(many=True, read_only=True)
    subject = SubjectSerializer(read_only=True)
    topic = TopicSerializer(read_only=True)
    
    class Meta:
        model = Question
        fields = [
            'id', 'question_text', 'question_type', 'difficulty',
            'topic', 'options', 'explanation', 'is_active',
            'created_at', 'updated_at'
        ]


class MockTestQuestionSerializer(serializers.ModelSerializer):
    question = QuestionSerializer(read_only=True)
    
    class Meta:
        model = MockTestQuestion
        fields = ['id', 'question', 'order', 'points']


class MockTestSerializer(serializers.ModelSerializer):
    questions = MockTestQuestionSerializer(many=True, read_only=True)
    subject = SubjectSerializer(read_only=True)
    
    class Meta:
        model = MockTest
        fields = [
            'id', 'name', 'description', 'test_type', 'duration_minutes',
            'total_questions', 'passing_score', 'is_free', 'price',
            'is_active', 'questions', 'created_at', 'updated_at'
        ]


class QuestionAttemptSerializer(serializers.ModelSerializer):
    question = QuestionSerializer(read_only=True)
    selected_option = QuestionOptionSerializer(read_only=True)
    
    class Meta:
        model = QuestionAttempt
        fields = [
            'id', 'question', 'selected_option', 'is_correct',
            'time_taken_seconds', 'created_at'
        ]


class MockTestAttemptSerializer(serializers.ModelSerializer):
    mock_test = MockTestSerializer(read_only=True)
    question_attempts = QuestionAttemptSerializer(many=True, read_only=True)
    
    class Meta:
        model = MockTestAttempt
        fields = [
            'id', 'user', 'mock_test', 'started_at', 'completed_at',
            'status', 'score', 'question_attempts', 'created_at'
        ]


class BookmarkedQuestionSerializer(serializers.ModelSerializer):
    question = QuestionSerializer(read_only=True)
    
    class Meta:
        model = BookmarkedQuestion
        fields = ['id', 'question', 'created_at']
