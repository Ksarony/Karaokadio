from django.contrib.auth.models import User
from django.db import models


class Station(models.Model):
	created_by = models.ForeignKey(User, on_delete=models.CASCADE)
	name = models.CharField(max_length=30)
	description = models.TextField(max_length=200)

	class Meta:
		ordering = ('name',)
