from django.urls import path
from . import views

urlpatterns = [
    path('', views.resources_page, name='resources_page'),
    path('api/', views.ResourceListAPI.as_view(), name='resources_api'),
    path('api/categories/', views.ResourceCategoryListAPI.as_view(), name='resource_categories_api'),
    path('api/universities/', views.UniversityListAPI.as_view(), name='universities_api'),
]
