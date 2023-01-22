from django.http import JsonResponse
from django.shortcuts import redirect, render, HttpResponse
from django.views.generic import ListView
from django.db import connection

from song.models import Song, Like, PlayHistory
from .models import Station
from .forms import CreateStationForm


class StationListView(ListView):
	model = Station
	paginate_by = 9

	def get_queryset(self):
		if not self.request.user.is_authenticated:
			return Station.objects.raw(
				f'''
					SELECT * FROM station_station
					ORDER BY name;
				'''
			)
		return Station.objects.raw(
			f'''
				SELECT * FROM station_station
				ORDER BY id IN (
					SELECT station_station.id FROM station_station 
					INNER JOIN station_station_subscribed_by 
					ON (station_station.id = station_station_subscribed_by.station_id) 
					WHERE station_station_subscribed_by.user_id = {self.request.user.id}
				) DESC, name
			'''
		)


def create(request):
	form = CreateStationForm()
	if request.method == "POST":
		form = CreateStationForm(request.POST)
		if form.is_valid():
			station = form.save(commit=False)
			station.created_by = request.user
			station.save()
			return redirect("station:list")
	return render(request, 'station/create_station.html', {'form': form})


def listen_station(request, id):
	user = request.user
	station = Station.objects.get(pk=id)

	if not station.song_set.exists():
		return render(request, 'station/listen_station.html', {'station': station})

	if not user.is_authenticated:
		song = random_song(station)
		return render(request, 'station/listen_station.html', {'station': station, 'song': song})

	song = recommend_song(station, user)
	liked = Like.objects.filter(song=song, liked_by=user).exists()
	PlayHistory(song=song, played_to=request.user).save()
	return render(request, 'station/listen_station.html', {'station': station, 'song': song, 'liked': liked})


def recommend_song(station, user):
	with connection.cursor() as cursor:
		cursor.execute("DROP VIEW IF EXISTS similar_songs;")
		cursor.execute("DROP VIEW IF EXISTS recent_songs;")
		cursor.execute(
			f'''
				CREATE VIEW similar_songs AS
				SELECT DISTINCT C.song_id id
				FROM song_like A, song_like B, song_like C
				WHERE A.liked_by_id = {user.id}
				AND A.song_id = B.song_id
				AND A.liked_by_id != B.liked_by_id
				AND B.liked_by_id = C.liked_by_id
				AND B.song_id != C.song_id;
			'''
		)
		cursor.execute(
			f'''
				CREATE VIEW recent_songs AS
				SELECT DISTINCT song_id FROM song_playhistory
				WHERE played_to_id = {user.id}
				AND played_at >= DATE('now', '-30 Day');
			'''
		)
		songs = Song.objects.raw(
			f'''
				SELECT * FROM (
					SELECT * FROM song_song
					INNER JOIN similar_songs
					ON (song_song.id = similar_songs.id)
					WHERE song_song.station_id = {station.id}
					AND song_song.id NOT IN recent_songs
					ORDER BY song_song.like_count DESC
					LIMIT 100
				)
				ORDER BY RANDOM()
				LIMIT 1;
			'''
		)

	if len(songs) > 0:
		return songs[0]

	songs = Song.objects.raw(
		f'''
			SELECT * FROM (
				SELECT * FROM song_song
				WHERE station_id = {station.id}
				AND id NOT IN recent_songs
				ORDER BY song_song.like_count DESC
				LIMIT 100
			)
			ORDER BY RANDOM()
			LIMIT 1;
		'''
	)

	if len(songs) > 0:
		return songs[0]

	return random_song(station)


def random_song(station):
	return station.song_set.order_by('?').first()


def subscribe(request, id):
	if not request.user.is_authenticated:
		return JsonResponse({"error": 'Unauthorized'}, status=401)
	station = Station.objects.get(pk=id)
	station.subscribed_by.add(request.user)
	return JsonResponse({"success": 'Subscribed successfully'}, status=200)


def delete_station(request, id):
	if not request.user.is_authenticated:
		return JsonResponse({"error": 'Unauthorized'}, status=401)
	station = Station.objects.get(pk=id)
	station.delete()
	return redirect("station:list")
