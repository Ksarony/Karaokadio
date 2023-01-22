from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView

from .forms import UploadForm
from .models import Song, Like


class SongListView(ListView):
	model = Song
	paginate_by = 9

	def get_queryset(self):
		qs = super().get_queryset()
		return qs.filter(created_by=self.request.user)


def upload(request):
	form = UploadForm()
	if request.method == "POST":
		form = UploadForm(request.POST, request.FILES)
		if form.is_valid():
			song = form.save(commit=False)
			song.created_by = request.user
			song.save()
			return redirect("song:list")
	return render(request=request, template_name="song/upload.html", context={'form': form})


def like(request, id):
	user = request.user
	song = Song.objects.get(pk=id)
	if Like.objects.filter(song=song, liked_by=user).exists():
		return JsonResponse({"error": 'Already liked'}, status=409)
	Like(song=song, liked_by=request.user).save()
	song.like_count += 1
	song.save()
	return JsonResponse({"success": 'Liked successfully'}, status=200)


def delete(request, id):
	song = Song.objects.get(pk=id)
	song.delete()
	return redirect("song:list")
