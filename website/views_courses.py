from django.shortcuts import render
from questions.models import Subject
from resources.models import University, Resource


# Step 1: University selection
def courses_page(request):
    universities = list(University.objects.filter(level='bachelors').order_by('name'))
    return render(request, 'courses.html', {
        'universities': universities,
    })

# Step 2: Field selection for a university
def university_fields(request, university_id):
    university = University.objects.get(id=university_id)
    fields = [
        {'key': 'computer', 'label': 'Computer Engineering', 'icon': 'fa-microchip'},
        {'key': 'software', 'label': 'Software Engineering', 'icon': 'fa-code'},
        {'key': 'it', 'label': 'Information Technology', 'icon': 'fa-network-wired'},
    ]
    return render(request, 'courses/field_detail.html', {
        'university': university,
        'fields': fields,
    })

# Step 3: Semester selection for a university and field
def university_semesters(request, university_id, field):
    university = University.objects.get(id=university_id)
    semesters = list(range(1, 9))
    return render(request, 'courses/semester_detail.html', {
        'university': university,
        'field': field,
        'semesters': semesters,
    })
