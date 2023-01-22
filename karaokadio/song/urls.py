from django.urls import path
from . import views, apps
from .views import SongListView

app_name = apps.SongConfig.name

urlpatterns = [
	path('list/', SongListView.as_view(), name='list'),
	path('upload/', views.upload, name='upload'),
	path('like/<id>', views.like, name='like'),
	path('delete/<id>', views.delete, name='delete'),
]
