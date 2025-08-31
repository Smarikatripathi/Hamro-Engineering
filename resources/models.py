
from django.db import models

class University(models.Model):
	name = models.CharField(max_length=255)
	level = models.CharField(max_length=50, choices=[('bachelors', 'Bachelors'), ('masters', 'Masters')])

	def __str__(self):
		return f"{self.name} ({self.level})"


class ResourceCategory(models.Model):
	CATEGORY_TYPE_CHOICES = [
		('entrance', 'Entrance'),
		('notes', 'Notes'),
	]
	name = models.CharField(max_length=100)
	type = models.CharField(max_length=20, choices=CATEGORY_TYPE_CHOICES, default='notes')
	description = models.TextField(blank=True)

	def __str__(self):
		return f"{self.name} ({self.get_type_display()})"

class Resource(models.Model):
	title = models.CharField(max_length=255)
	category = models.ForeignKey(ResourceCategory, on_delete=models.CASCADE)
	university = models.ForeignKey(University, on_delete=models.CASCADE, null=True, blank=True)
	file = models.FileField(upload_to='resources/', blank=True, null=True)
	link = models.URLField(blank=True, null=True)
	description = models.TextField(blank=True)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.title
