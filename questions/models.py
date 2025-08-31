from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()


class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    icon = models.CharField(max_length=50, blank=True, null=True)  # For FontAwesome icons
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Topic(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='topics')
    name = models.CharField(max_length=100)
    description = models.TextField()
    difficulty_level = models.CharField(
        max_length=10,
        choices=[
            ('easy', 'Easy'),
            ('medium', 'Medium'),
            ('hard', 'Hard'),
        ],
        default='medium'
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['subject', 'name']
        unique_together = ['subject', 'name']
    
    def __str__(self):
        return f"{self.subject.name} - {self.name}"


class Question(models.Model):
    QUESTION_TYPE_CHOICES = [
        ('mcq', 'Multiple Choice Question'),
        ('true_false', 'True/False'),
        ('numerical', 'Numerical'),
    ]
    
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]
    
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    question_type = models.CharField(max_length=15, choices=QUESTION_TYPE_CHOICES, default='mcq')
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='medium')
    marks = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(10)])
    explanation = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['topic', 'difficulty', 'created_at']
    
    def __str__(self):
        return f"{self.topic.name} - {self.question_text[:50]}..."


class QuestionOption(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    option_text = models.CharField(max_length=500)
    is_correct = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['question', 'order']
        unique_together = ['question', 'order']
    
    def __str__(self):
        return f"{self.question.id} - Option {self.order}: {self.option_text[:30]}..."


class MockTest(models.Model):
    TEST_TYPE_CHOICES = [
        ('IOE', 'Institute of Engineering'),
        ('KU', 'Kathmandu University'),
        ('PU', 'Purbanchal University'),
        ('PoU', 'Pokhara University'),
        ('custom', 'Custom Test'),
    ]
    
    name = models.CharField(max_length=200)
    description = models.TextField()
    test_type = models.CharField(max_length=10, choices=TEST_TYPE_CHOICES)
    duration_minutes = models.IntegerField(validators=[MinValueValidator(15), MaxValueValidator(300)])
    total_questions = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(200)])
    passing_score = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    is_free = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} ({self.get_test_type_display()})"


class MockTestQuestion(models.Model):
    mock_test = models.ForeignKey(MockTest, on_delete=models.CASCADE, related_name='test_questions')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    order = models.IntegerField()
    marks = models.IntegerField(default=1)
    
    class Meta:
        ordering = ['mock_test', 'order']
        unique_together = ['mock_test', 'order']
    
    def __str__(self):
        return f"{self.mock_test.name} - Q{self.order}"


class MockTestAttempt(models.Model):
    STATUS_CHOICES = [
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('abandoned', 'Abandoned'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='test_attempts')
    mock_test = models.ForeignKey(MockTest, on_delete=models.CASCADE, related_name='attempts')
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='in_progress')
    score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    total_marks = models.IntegerField(null=True, blank=True)
    accuracy_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    time_taken_minutes = models.IntegerField(null=True, blank=True)
    
    class Meta:
        ordering = ['-started_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.mock_test.name} ({self.status})"


class QuestionAttempt(models.Model):
    test_attempt = models.ForeignKey(MockTestAttempt, on_delete=models.CASCADE, related_name='question_attempts')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.ForeignKey(QuestionOption, on_delete=models.SET_NULL, null=True, blank=True)
    is_correct = models.BooleanField(null=True, blank=True)
    time_taken_seconds = models.IntegerField(null=True, blank=True)
    is_marked_for_review = models.BooleanField(default=False)
    answered_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['test_attempt', 'question']
    
    def __str__(self):
        return f"{self.test_attempt.id} - Q{self.question.id}"


class BookmarkedQuestion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookmarked_questions')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'question']
    
    def __str__(self):
        return f"{self.user.username} - {self.question.id}"
