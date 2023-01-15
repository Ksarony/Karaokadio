from django.shortcuts import render, redirect
from .forms import UploadForm
from .models import Song


def upload(request):
	form = None
	user = request.user
	songs = Song.objects.filter(user=user)
	if request.method == "POST":
		form = UploadForm(request.POST, request.FILES)
		if form.is_valid():
			song = form.save(commit=False)
			song.user = user
			song.save()
			return redirect("/")
	else:
		form = UploadForm()
	return render(request=request, template_name="song/upload.html", context={'form': form, 'songs': songs})
