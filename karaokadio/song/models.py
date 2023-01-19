from django.contrib.auth.models import User
from django.db import models
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
import uuid

from station.models import Station


def song_path(instance, filename):
	return 'songs/{0}_{1}'.format(uuid.uuid4(), filename)


def song_size_limiter(value):
	limit = 10 * 1024 * 1024
	if value.size > limit:
		raise ValidationError('File is too large, size should not exceed 10 MB.')


class Song(models.Model):
	created_by = models.ForeignKey(User, on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)
	title = models.CharField(max_length=100)
	station = models.ForeignKey(Station, on_delete=models.SET_NULL, null=True)
	file = models.FileField(
		upload_to=song_path,
		validators=[
			FileExtensionValidator(allowed_extensions=['mp3', 'mp4', 'wav', 'aac', 'wma', 'flac', 'm4a']),
			song_size_limiter
		]
	)
