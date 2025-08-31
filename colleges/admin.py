from django.contrib import admin
from .models import College, EngineeringProgram, EntranceExam


@admin.register(College)
class CollegeAdmin(admin.ModelAdmin):
    list_display = ['name', 'university', 'location', 'is_active', 'created_at']
    list_filter = ['university', 'is_active', 'created_at']
    search_fields = ['name', 'location', 'description']
    ordering = ['name']


@admin.register(EngineeringProgram)
class EngineeringProgramAdmin(admin.ModelAdmin):
    list_display = ['name', 'college', 'program_type', 'duration_years', 'is_active', 'created_at']
    list_filter = ['program_type', 'duration_years', 'is_active', 'college__university', 'created_at']
    search_fields = ['name', 'college__name', 'description']
    ordering = ['college__name', 'name']


@admin.register(EntranceExam)
class EntranceExamAdmin(admin.ModelAdmin):
    list_display = ['name', 'exam_type', 'college', 'exam_date', 'is_active', 'created_at']
    list_filter = ['exam_type', 'college', 'is_active', 'created_at']
    search_fields = ['name', 'description', 'college__name']
    ordering = ['-exam_date']
