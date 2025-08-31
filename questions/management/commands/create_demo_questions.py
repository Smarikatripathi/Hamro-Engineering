from django.core.management.base import BaseCommand
from questions.models import Subject, Topic, Question, QuestionOption, MockTest, MockTestQuestion
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Create demo subjects, topics, questions, and a mock test.'

    def handle(self, *args, **kwargs):
        # Create a demo subject
        subject, _ = Subject.objects.get_or_create(
            name='Mathematics',
            defaults={'description': 'Math subject for demo', 'icon': 'fa-calculator'}
        )
        # Create a topic
        topic, _ = Topic.objects.get_or_create(
            subject=subject,
            name='Algebra',
            defaults={'description': 'Algebra basics', 'difficulty_level': 'easy'}
        )
        # Create questions
        q1 = Question.objects.create(
            topic=topic,
            question_text='What is the value of x if 2x + 3 = 7?',
            question_type='mcq',
            difficulty='easy',
            marks=1,
            explanation='2x + 3 = 7 => 2x = 4 => x = 2.'
        )
        QuestionOption.objects.create(question=q1, option_text='1', is_correct=False, order=1)
        QuestionOption.objects.create(question=q1, option_text='2', is_correct=True, order=2)
        QuestionOption.objects.create(question=q1, option_text='3', is_correct=False, order=3)
        QuestionOption.objects.create(question=q1, option_text='4', is_correct=False, order=4)

        q2 = Question.objects.create(
            topic=topic,
            question_text='What is (a+b)^2?',
            question_type='mcq',
            difficulty='easy',
            marks=1,
            explanation='(a+b)^2 = a^2 + 2ab + b^2.'
        )
        QuestionOption.objects.create(question=q2, option_text='a^2 + b^2', is_correct=False, order=1)
        QuestionOption.objects.create(question=q2, option_text='a^2 + 2ab + b^2', is_correct=True, order=2)
        QuestionOption.objects.create(question=q2, option_text='a^2 - 2ab + b^2', is_correct=False, order=3)
        QuestionOption.objects.create(question=q2, option_text='2a^2 + 2b^2', is_correct=False, order=4)

        # Create a mock test
        mock_test = MockTest.objects.create(
            name='Demo Math Mock Test',
            description='A demo mock test for Mathematics.',
            test_type='IOE',
            duration_minutes=30,
            total_questions=2,
            passing_score=50,
            is_free=True,
            price=0.0,
            is_active=True
        )
        MockTestQuestion.objects.create(mock_test=mock_test, question=q1, order=1, marks=1)
        MockTestQuestion.objects.create(mock_test=mock_test, question=q2, order=2, marks=1)

        self.stdout.write(self.style.SUCCESS('Demo questions and mock test created!'))
