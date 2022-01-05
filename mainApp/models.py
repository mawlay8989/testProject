from django.db import models
from django.utils import timezone
from django.urls import reverse

from django.contrib.auth.models import User

class Task(models.Model):
	owner = models.ForeignKey(User, on_delete=models.CASCADE)
	category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.CASCADE)
	title = models.CharField(max_length=100)
	description = models.TextField()
	date = models.DateTimeField(default=timezone.now)
  
	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse("task-show-view", args=[self.pk])

class Category(models.Model):
	name = models.CharField(max_length=100)
	slug = models.SlugField()

	def __str__(self):
		return self.name