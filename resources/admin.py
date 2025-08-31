from django.contrib import admin
from .models import University, ResourceCategory, Resource

@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
	list_display = ('name', 'level')
	search_fields = ('name',)
	list_filter = ('level',)

@admin.register(ResourceCategory)
class ResourceCategoryAdmin(admin.ModelAdmin):
	list_display = ('name',)
	search_fields = ('name',)

@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
	list_display = ('title', 'category', 'university', 'created_at')
	search_fields = ('title',)
	list_filter = ('category', 'university')
