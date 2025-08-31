from django.core.management.base import BaseCommand
from resources.models import University, ResourceCategory, Resource

class Command(BaseCommand):
    help = 'Create demo resource categories and notes for each section.'

    def handle(self, *args, **kwargs):
        # Universities
        btu, _ = University.objects.get_or_create(name='TU', level='bachelors')
        bpu, _ = University.objects.get_or_create(name='PU', level='bachelors')
        mtu, _ = University.objects.get_or_create(name='TU', level='masters')
        mpu, _ = University.objects.get_or_create(name='PU', level='masters')

        # Categories
        b_entrance, _ = ResourceCategory.objects.get_or_create(name='Bachelor Entrance', type='entrance')
        b_notes, _ = ResourceCategory.objects.get_or_create(name='Engineering Notes', type='notes')
        m_entrance, _ = ResourceCategory.objects.get_or_create(name='Masters Entrance', type='entrance')
        m_notes, _ = ResourceCategory.objects.get_or_create(name='Masters Notes', type='notes')

        # Demo Resources
        Resource.objects.get_or_create(
            title='Sample Bachelor Entrance Syllabus',
            category=b_entrance,
            university=btu,
            description='Demo syllabus for bachelor entrance exam.',
            link='https://example.com/bachelor-entrance-syllabus.pdf'
        )
        Resource.objects.get_or_create(
            title='Sample Engineering Notes (Bachelors)',
            category=b_notes,
            university=bpu,
            description='Demo notes for bachelor engineering students.',
            link='https://example.com/bachelor-notes.pdf'
        )
        Resource.objects.get_or_create(
            title='Sample Masters Entrance Syllabus',
            category=m_entrance,
            university=mtu,
            description='Demo syllabus for masters entrance exam.',
            link='https://example.com/masters-entrance-syllabus.pdf'
        )
        Resource.objects.get_or_create(
            title='Sample Masters Notes',
            category=m_notes,
            university=mpu,
            description='Demo notes for masters engineering students.',
            link='https://example.com/masters-notes.pdf'
        )
        self.stdout.write(self.style.SUCCESS('Demo resource categories and notes created.'))
