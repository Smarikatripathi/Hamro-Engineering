from django.shortcuts import render
from questions.models import Subject
from resources.models import University, Resource

def courses_page(request):  # Removing the stray definition
    semesters = list(range(1, 9))
    fields = [
        {'key': 'computer', 'label': 'Computer Engineering', 'icon': 'fa-microchip'},
        {'key': 'software', 'label': 'Software Engineering', 'icon': 'fa-code'},
        {'key': 'it', 'label': 'Information Technology', 'icon': 'fa-network-wired'},
    ]
    universities = list(University.objects.filter(level='bachelors').order_by('name'))

    # Structure: {semester: {field: {university_id: [subjects]}}}
    data = {}
    for sem in semesters:
        data[sem] = {}
        for field in fields:
            field_key = field['key']
            data[sem][field_key] = {}
            for uni in universities:
                subjects = Subject.objects.filter(semester=sem, field=field_key, is_active=True)
                # Optionally, filter by university if you add a university field to Subject
                data[sem][field_key][uni.id] = subjects

    return render(request, 'courses.html', {
        'semesters': semesters,
        'fields': fields,
        'universities': universities,
        'data': data,
    })
