from django.urls import re_path
from . import views, apps

app_name = apps.HomeConfig.name

urlpatterns = [
	re_path(r'^$', views.index, name='index'),
	re_path(r'^login/$', views.login, name='login'),
	re_path(r'^signup/$', views.signup, name='signup'),
	re_path(r'^logout/$', views.logout, name='logout'),
]
