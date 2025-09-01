from django.core.management.base import BaseCommand
from questions.models import Subject

SUBJECTS = {
    1: [
        "Calculus I",
        "Digital Logic",
        "Programming in C",
        "Basic Electrical Engineering",
        "Computer Workshop",
        "Communication Technique",
        "Electronics Devices and Circuits",
    ],
    2: [
        "Algebra and Geometry",
        "Applied Physics",
        "Applied Chemistry",
        "Basic Engineering Drawing",
        "Object Oriented Programming in C++",
        "Data Structure and Algorithm",
        "Instrumentation",
    ],
    3: [
        "Calculus II",
        "Database Management System",
        "Operating Systems",
        "Microprocessor and Assembly Language Programming",
        "Computer Graphics",
        "Data Communication",
    ],
    4: [
        "Applied Mathematics",
        "Numerical Methods",
        "Advanced Programming with Java",
        "Theory of Computation",
        "Computer Architecture",
        "Research Fundamentals",
    ],
    5: [
        "Probability and Statistics",
        "Embedded System",
        "Engineering Management",
        "Artificial Intelligence",
        "Digital Signal Analysis and Processing",
        "Software Engineering",
    ],
    6: [
        "Image Processing and Pattern Recognition",
        "Machine Learning",
        "Compiler Design",
        "Computer Networks",
        "Simulation and Modeling",
        "Elective I",
        "Project I",
    ],
    7: [
        "Entrepreneurship and Professional Practice",
        "Engineering Economics",
        "Network and Cyber Security",
        "Cloud Computing and Virtualization",
        "Data Science and Analytics",
        "Elective II",
    ],
    8: [
        "Elective III",
        "Internship",
        "Project II",
    ],
}

class Command(BaseCommand):
    help = 'Populate Computer Engineering subjects for each semester.'

    def handle(self, *args, **kwargs):
        created = 0
        for semester, subjects in SUBJECTS.items():
            for name in subjects:
                obj, was_created = Subject.objects.get_or_create(
                    name=name,
                    defaults={
                        'semester': semester,
                        'field': 'computer',
                        'description': '',
                        'is_active': True,
                    }
                )
                if was_created:
                    created += 1
        self.stdout.write(self.style.SUCCESS(f"Added {created} Computer Engineering subjects."))
