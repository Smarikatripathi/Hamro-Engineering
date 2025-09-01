
from django.shortcuts import render
from rest_framework import generics
from .models import Resource, ResourceCategory, University
from .serializers import ResourceSerializer, ResourceCategorySerializer, UniversitySerializer

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .models import Resource, ResourceCategory, University

def resources_page(request):
	categories = ResourceCategory.objects.all()
	universities = University.objects.all()
	resources = Resource.objects.all().order_by('-created_at')
	from questions.models import Subject
	semesters = list(range(1, 9))
	subjects_by_semester = {sem: Subject.objects.filter(semester=sem, is_active=True).order_by('name') for sem in semesters}

	if request.method == 'POST':
		if not request.user.is_authenticated:
			messages.error(request, 'You must be logged in to upload resources.')
			return redirect('resources_page')
		title = request.POST.get('title')
		category_id = request.POST.get('category')
		university_id = request.POST.get('university')
		description = request.POST.get('description')
		link = request.POST.get('link')
		file = request.FILES.get('file')
		category = ResourceCategory.objects.filter(id=category_id).first()
		university = University.objects.filter(id=university_id).first() if university_id else None
		if not title or not category:
			messages.error(request, 'Title and category are required.')
		elif not file and not link:
			messages.error(request, 'Please provide a file or a link.')
		else:
			Resource.objects.create(
				title=title,
				category=category,
				university=university,
				file=file,
				link=link,
				description=description
			)
			messages.success(request, 'Resource uploaded successfully!')
			return redirect('resources_page')

	return render(request, 'resources/resources.html', {
		'categories': categories,
		'universities': universities,
		'resources': resources,
		'semesters': semesters,
		'subjects_by_semester': subjects_by_semester,
	})

class ResourceListAPI(generics.ListAPIView):
	queryset = Resource.objects.all().order_by('-created_at')
	serializer_class = ResourceSerializer

class ResourceCategoryListAPI(generics.ListAPIView):
	queryset = ResourceCategory.objects.all()
	serializer_class = ResourceCategorySerializer

class UniversityListAPI(generics.ListAPIView):
	queryset = University.objects.all()
	serializer_class = UniversitySerializer
