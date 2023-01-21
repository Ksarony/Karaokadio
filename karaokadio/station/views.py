from django.http import JsonResponse
from django.shortcuts import redirect, render, HttpResponse
from django.views.generic import ListView
import random

from song.models import Song
from .models import Station
from .forms import CreateStationForm


class StationListView(ListView):
	model = Station
	paginate_by = 9

	def get_queryset(self):
		qs = super().get_queryset()
		return qs.order_by('name')


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
	station = Station.objects.get(pk=id)
	song_pks = station.song_set.values_list('pk', flat=True)
	random_pk = random.choice(song_pks)
	song = Song.objects.get(pk=random_pk)
	return render(request, 'station/listen_station.html', {'station': station, 'song': song})


def subscribe(request, id):
	station = Station.objects.get(pk=id)
	station.subscribed_by.add(request.user)
	return JsonResponse({"success": 'Subscribed successfully'}, status=200)


def delete_station(request, id):
	station = Station.objects.get(pk=id)
	station.delete()
	return redirect("station:list")
