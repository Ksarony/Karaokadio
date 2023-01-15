from django.urls import path
from . import views, apps

app_name = apps.StationConfig.name

urlpatterns = [
	path('', views.index, name='index'),
	path('listen/<id>', views.listen_station, name='listen'),
	path('delete/<id>', views.delete_station, name='delete'),
]
