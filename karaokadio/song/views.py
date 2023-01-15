from django.shortcuts import render, redirect
from .forms import UploadForm
from .models import Song


def upload(request):
	user = request.user
	form = UploadForm()
	if request.method == "POST":
		form = UploadForm(request.POST, request.FILES)
		if form.is_valid():
			song = form.save(commit=False)
			song.created_by = user
			song.save()
			return redirect("song:upload")
	songs = Song.objects.filter(created_by=user)
	return render(request=request, template_name="song/upload.html", context={'form': form, 'songs': songs})


def delete(request, id):
	song = Song.objects.get(pk=id)
	song.delete()
	return redirect("song:upload")
