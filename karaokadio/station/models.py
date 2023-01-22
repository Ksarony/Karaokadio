from django.contrib.auth.models import User
from django.db import models


class Station(models.Model):
	created_by = models.ForeignKey(User, on_delete=models.CASCADE)
	name = models.CharField(max_length=30, unique=True)
	description = models.TextField(max_length=200)
	subscribed_by = models.ManyToManyField(User, related_name='subscribed_stations')

	class Meta:
		ordering = ('name',)

	def __str__(self):
		return self.name
