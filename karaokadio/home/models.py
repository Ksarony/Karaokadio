from django.db import models


class UserProfile(models.Model):
	userid = models.CharField(max_length=20)
	password = models.CharField(max_length=25)

	class Meta:
		ordering = ['userid']
		db_table = 'user_profile'

	def __str__(self):
		return self.id

	def get_absolute_url(self):
		return "/user/%i" % self.id
