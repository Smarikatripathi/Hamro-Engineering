from django.db import models


class College(models.Model):
    UNIVERSITY_CHOICES = (
        ('TU', 'Tribhuvan University'),
        ('PU', 'Purbanchal University'),
        ('KU', 'Kathmandu University'),
        ('PoU', 'Pokhara University'),
        ('MU', 'Mid-Western University'),
        ('FU', 'Far-Western University'),
        ('LU', 'Lumbini University'),
    )
    
    name = models.CharField(max_length=200)
    university = models.CharField(max_length=3, choices=UNIVERSITY_CHOICES)
    location = models.CharField(max_length=200)
    established_year = models.IntegerField()
    website = models.URLField(blank=True, null=True)
    description = models.TextField()
    logo = models.ImageField(upload_to='college_logos/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.get_university_display()})"


class EngineeringProgram(models.Model):
    PROGRAM_TYPE_CHOICES = (
        ('BE', 'Bachelor of Engineering'),
        ('BArch', 'Bachelor of Architecture'),
        ('BTech', 'Bachelor of Technology'),
    )
    
    college = models.ForeignKey(College, on_delete=models.CASCADE, related_name='programs')
    name = models.CharField(max_length=100)
    program_type = models.CharField(max_length=5, choices=PROGRAM_TYPE_CHOICES)
    duration_years = models.IntegerField(default=4)
    total_seats = models.IntegerField()
    available_seats = models.IntegerField()
    fee_structure = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} - {self.college.name}"


class EntranceExam(models.Model):
    EXAM_TYPE_CHOICES = (
        ('IOE', 'Institute of Engineering'),
        ('KU', 'Kathmandu University'),
        ('PU', 'Purbanchal University'),
        ('PoU', 'Pokhara University'),
    )
    
    name = models.CharField(max_length=100)
    exam_type = models.CharField(max_length=3, choices=EXAM_TYPE_CHOICES)
    college = models.ForeignKey(College, on_delete=models.CASCADE, related_name='entrance_exams')
    exam_date = models.DateField()
    registration_deadline = models.DateField()
    total_questions = models.IntegerField()
    duration_minutes = models.IntegerField()
    passing_score = models.IntegerField()
    fee_amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-exam_date']
    
    def __str__(self):
        return f"{self.name} - {self.get_exam_type_display()}"
