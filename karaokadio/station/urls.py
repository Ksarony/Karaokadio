from django.urls import path
from . import views, apps
from .views import StationListView

app_name = apps.StationConfig.name

urlpatterns = [
	path('list', StationListView.as_view(), name='list'),
	path('create', views.create, name='create'),
	path('listen/<id>', views.listen_station, name='listen'),
	path('subscribe/<id>', views.subscribe, name='subscribe'),
	path('delete/<id>', views.delete_station, name='delete'),
]
