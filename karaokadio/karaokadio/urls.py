from django.contrib import admin
from django.urls import include, path, re_path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
	path("admin/", admin.site.urls),
	re_path(r'^', include('home.urls')),
	re_path(r'^song/', include('song.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
