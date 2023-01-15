from django.urls import path
from . import views, apps

app_name = apps.SongConfig.name

urlpatterns = [
	path('upload', views.upload, name='upload'),
	path('delete/<id>', views.delete, name='delete'),
]
