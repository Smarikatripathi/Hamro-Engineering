from rest_framework import serializers
from .models import College, EngineeringProgram, EntranceExam


class CollegeSerializer(serializers.ModelSerializer):
    class Meta:
        model = College
        fields = [
            'id', 'name', 'description', 'location', 'college_type',
            'established_year', 'website', 'contact_email', 'contact_phone',
            'is_active', 'created_at', 'updated_at'
        ]


class EngineeringProgramSerializer(serializers.ModelSerializer):
    college = CollegeSerializer(read_only=True)
    
    class Meta:
        model = EngineeringProgram
        fields = [
            'id', 'name', 'description', 'college', 'program_type',
            'duration_years', 'total_seats', 'is_active', 'created_at'
        ]


class EntranceExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntranceExam
        fields = [
            'id', 'name', 'description', 'exam_type', 'conducting_body',
            'exam_date', 'registration_deadline', 'is_active', 'created_at'
        ]
