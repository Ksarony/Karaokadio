from django import forms
from .models import Song


class UploadForm(forms.ModelForm):
	class Meta:
		model = Song
		fields = ['title', 'station', 'file']
