from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import College, EngineeringProgram, EntranceExam
from .serializers import (
    CollegeSerializer, EngineeringProgramSerializer, EntranceExamSerializer
)


class CollegeListView(generics.ListCreateAPIView):
    queryset = College.objects.filter(is_active=True)
    serializer_class = CollegeSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['location', 'college_type', 'is_active']
    search_fields = ['name', 'description', 'location']
    ordering_fields = ['name', 'created_at']


class CollegeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = College.objects.all()
    serializer_class = CollegeSerializer
    permission_classes = [permissions.IsAuthenticated]


class EngineeringProgramListView(generics.ListCreateAPIView):
    queryset = EngineeringProgram.objects.filter(is_active=True)
    serializer_class = EngineeringProgramSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['college', 'program_type', 'duration_years', 'is_active']
    search_fields = ['name', 'description']


class EngineeringProgramDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = EngineeringProgram.objects.all()
    serializer_class = EngineeringProgramSerializer
    permission_classes = [permissions.IsAuthenticated]


class EntranceExamListView(generics.ListCreateAPIView):
    queryset = EntranceExam.objects.filter(is_active=True)
    serializer_class = EntranceExamSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['exam_type', 'conducting_body', 'is_active']
    search_fields = ['name', 'description', 'conducting_body']


class EntranceExamDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = EntranceExam.objects.all()
    serializer_class = EntranceExamSerializer
    permission_classes = [permissions.IsAuthenticated]
