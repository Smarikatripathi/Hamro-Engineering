from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.utils import timezone

from .models import Question, QuestionOption, Subject, Topic, MockTest, MockTestQuestion, MockTestAttempt, QuestionAttempt, BookmarkedQuestion
from .serializers import (
    QuestionSerializer, QuestionOptionSerializer, SubjectSerializer, TopicSerializer,
    MockTestSerializer, MockTestQuestionSerializer, MockTestAttemptSerializer,
    QuestionAttemptSerializer, BookmarkedQuestionSerializer
)


class QuestionListView(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['topic__subject', 'topic', 'difficulty', 'question_type']
    search_fields = ['question_text', 'explanation']
    ordering_fields = ['created_at', 'difficulty']


class QuestionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticated]


class SubjectListView(generics.ListCreateAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [permissions.IsAuthenticated]


class SubjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [permissions.IsAuthenticated]


class TopicListView(generics.ListCreateAPIView):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    permission_classes = [permissions.IsAuthenticated]


class TopicDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    permission_classes = [permissions.IsAuthenticated]


class MockTestListView(generics.ListCreateAPIView):
    queryset = MockTest.objects.all()
    serializer_class = MockTestSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['test_type', 'is_active']
    search_fields = ['title', 'description']


class MockTestDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MockTest.objects.all()
    serializer_class = MockTestSerializer
    permission_classes = [permissions.IsAuthenticated]


class StartMockTestView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, pk):
        mock_test = get_object_or_404(MockTest, pk=pk)
        
        # Check if user already has an active attempt
        active_attempt = MockTestAttempt.objects.filter(
            user=request.user,
            mock_test=mock_test,
            status='in_progress'
        ).first()
        
        if active_attempt:
            return Response({
                'message': 'You already have an active attempt for this test',
                'attempt_id': active_attempt.id
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Create new attempt
        attempt = MockTestAttempt.objects.create(
            user=request.user,
            mock_test=mock_test,
            started_at=timezone.now()
        )
        
        return Response({
            'message': 'Mock test started successfully',
            'attempt_id': attempt.id
        }, status=status.HTTP_201_CREATED)


class SubmitMockTestView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, pk):
        attempt = get_object_or_404(MockTestAttempt, pk=pk, user=request.user)
        
        if attempt.status == 'completed':
            return Response({
                'message': 'This attempt is already completed'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Mark attempt as completed
        attempt.status = 'completed'
        attempt.completed_at = timezone.now()
        attempt.save()
        
        # Calculate score
        total_questions = attempt.mock_test.questions.count()
        correct_answers = attempt.question_attempts.filter(is_correct=True).count()
        score = (correct_answers / total_questions) * 100 if total_questions > 0 else 0
        
        attempt.score = score
        attempt.save()
        
        return Response({
            'message': 'Mock test submitted successfully',
            'score': score,
            'total_questions': total_questions,
            'correct_answers': correct_answers
        }, status=status.HTTP_200_OK)


class PracticeView(generics.ListAPIView):
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        subject_id = self.kwargs['subject_id']
        return Question.objects.filter(subject_id=subject_id).order_by('?')[:10]


class BookmarkQuestionView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, question_id):
        question = get_object_or_404(Question, pk=question_id)
        user = request.user
        
        # Toggle bookmark
        bookmark, created = BookmarkedQuestion.objects.get_or_create(
            user=user,
            question=question
        )
        
        if not created:
            bookmark.delete()
            return Response({
                'message': 'Question removed from bookmarks'
            }, status=status.HTTP_200_OK)
        
        return Response({
            'message': 'Question added to bookmarks'
        }, status=status.HTTP_201_CREATED)


class BookmarkedQuestionsView(generics.ListAPIView):
    serializer_class = BookmarkedQuestionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return BookmarkedQuestion.objects.filter(user=self.request.user)
