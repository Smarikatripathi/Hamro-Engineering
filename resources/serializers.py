from rest_framework import serializers
from .models import University, ResourceCategory, Resource

class UniversitySerializer(serializers.ModelSerializer):
    class Meta:
        model = University
        fields = '__all__'

class ResourceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceCategory
        fields = '__all__'

class ResourceSerializer(serializers.ModelSerializer):
    category = ResourceCategorySerializer(read_only=True)
    university = UniversitySerializer(read_only=True)

    class Meta:
        model = Resource
        fields = '__all__'
