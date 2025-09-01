from rest_framework import generics, permissions, status
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect
from .forms import PDFUploadForm
import pdfplumber
@method_decorator(staff_member_required, name='dispatch')
class PDFUploadView(generics.GenericAPIView):
    """Staff-only view for uploading a PDF and extracting MCQs."""
    def get(self, request):
        form = PDFUploadForm()
        return render(request, 'questions/pdf_upload.html', {'form': form})

    def post(self, request):
        form = PDFUploadForm(request.POST, request.FILES)
        imported_count = 0
        errors = []
        if form.is_valid():
            pdf_file = form.cleaned_data['pdf_file']
            with pdfplumber.open(pdf_file) as pdf:
                text = "\n".join(page.extract_text() or '' for page in pdf.pages)

            # Simple MCQ parser: expects format as described
            import re
            question_blocks = re.split(r'\n\d+\. ', text)
            for block in question_blocks:
                if not block.strip():
                    continue
                # Extract question, options, and answer
                lines = block.strip().split('\n')
                if len(lines) < 3:
                    continue
                question_text = lines[0].strip()
                options = []
                answer = None
                for line in lines[1:]:
                    opt_match = re.match(r'([A-D])\)\s*(.+)', line)
                    if opt_match:
                        options.append((opt_match.group(1), opt_match.group(2).strip()))
                    ans_match = re.match(r'Answer[:\s]+([A-D])', line, re.IGNORECASE)
                    if ans_match:
                        answer = ans_match.group(1)
                if not question_text or len(options) < 2 or not answer:
                    errors.append(f"Skipped: '{question_text[:40]}...' (missing options/answer)")
                    continue
                # Create Question and Options (assign to first Subject/Topic for demo)
                from .models import Subject, Topic, Question, QuestionOption
                subject = Subject.objects.first()
                topic = Topic.objects.filter(subject=subject).first()
                if not subject or not topic:
                    errors.append("No Subject/Topic found. Please create at least one in admin.")
                    break
                q = Question.objects.create(
                    topic=topic,
                    question_text=question_text,
                    question_type='mcq',
                    difficulty='medium',
                    marks=1,
                    is_active=True,
                    created_by=request.user if request.user.is_authenticated else None
                )
                for idx, (opt_key, opt_text) in enumerate(options):
                    QuestionOption.objects.create(
                        question=q,
                        option_text=opt_text,
                        is_correct=(opt_key.upper() == answer.upper()),
                        order=idx+1
                    )
                imported_count += 1
            return render(request, 'questions/pdf_upload.html', {
                'form': form,
                'imported_count': imported_count,
                'errors': errors,
                'extracted_text': text
            })
        return render(request, 'questions/pdf_upload.html', {'form': form})
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
