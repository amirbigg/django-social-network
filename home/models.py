from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	body = models.TextField()
	slug = models.SlugField()
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f'{self.slug} - {self.updated}'
