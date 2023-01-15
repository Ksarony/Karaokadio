from django import forms
from .models import Station


class CreateStationForm(forms.ModelForm):
	class Meta:
		model = Station
		fields = ['name', 'description']
