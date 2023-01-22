from io import StringIO

from django.http import JsonResponse
from django.db import connection
from django.shortcuts import render, redirect
from django.views.generic import ListView
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from .forms import UploadForm
from .models import Song, Like


class SongListView(ListView):
	model = Song
	paginate_by = 9

	def get_queryset(self):
		if not self.request.user.is_authenticated:
			return Song.objects.none()
		qs = super().get_queryset()
		return qs.filter(created_by=self.request.user)


def upload(request):
	if not request.user.is_authenticated:
		return JsonResponse({"error": 'Unauthorized'}, status=401)
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
	if not request.user.is_authenticated:
		return JsonResponse({"error": 'Unauthorized'}, status=401)
	user = request.user
	song = Song.objects.get(pk=id)
	if Like.objects.filter(song=song, liked_by=user).exists():
		return JsonResponse({"error": 'Already liked'}, status=409)
	Like(song=song, liked_by=request.user).save()
	song.like_count += 1
	song.save()
	return JsonResponse({"success": 'Liked successfully'}, status=200)


def delete(request, id):
	if not request.user.is_authenticated:
		return JsonResponse({"error": 'Unauthorized'}, status=401)
	song = Song.objects.get(pk=id)
	song.delete()
	return redirect("song:list")


def stats(request):
	if not request.user.is_authenticated:
		return JsonResponse({"error": 'Unauthorized'}, status=401)

	with connection.cursor() as cursor:
		cursor.execute(
			f'''
				SELECT title, like_count FROM song_song
				WHERE created_by_id = {request.user.id}
				ORDER BY like_count
				LIMIT 10;
			'''
		)
		all_times_hit_df = pd.DataFrame(cursor.fetchall())

		cursor.execute(
			f'''
						SELECT title, COUNT(*) C FROM song_song
						LEFT OUTER JOIN song_like
						ON (song_song.id = song_like.song_id)
						WHERE song_song.created_by_id = {request.user.id}
						AND song_like.liked_at >= DATE('now', '-30 Day')
						GROUP BY song_song.id
						ORDER BY C
						LIMIT 10;
					'''
		)
		monthly_hit_df = pd.DataFrame(cursor.fetchall())

	all_times_hit = '' if all_times_hit_df.size == 0 else get_plot(all_times_hit_df, 'Your All-Time Hits')
	monthly_hit = '' if monthly_hit_df.size == 0 else get_plot(monthly_hit_df, 'Your Monthly Hits')
	return render(request=request, template_name="song/stats.html",
	              context={'all_times_hit': all_times_hit, 'monthly_hit': monthly_hit})


def get_plot(df, title):
	fig = plt.figure()
	songs = df[0]
	y_pos = np.arange(len(songs))
	likes = df[1]
	hbars = plt.barh(y_pos, likes, align='center', alpha=0.5)
	plt.bar_label(hbars, labels=songs, fontsize=10, padding=6)
	plt.gca().set_xlim(right=max(likes) + 10)
	plt.yticks(y_pos, '')
	plt.xlabel('Likes')
	plt.title(title)
	imgdata = StringIO()
	fig.savefig(imgdata, format='svg')
	imgdata.seek(0)
	return imgdata.getvalue()
