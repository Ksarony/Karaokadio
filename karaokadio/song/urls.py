from django.urls import path
from . import views, apps
from .views import SongListView

app_name = apps.SongConfig.name

urlpatterns = [
	path('list', SongListView.as_view(), name='list'),
	path('play/<id>', views.play, name='play'),
	path('upload', views.upload, name='upload'),
	path('delete/<id>', views.delete, name='delete'),
]
