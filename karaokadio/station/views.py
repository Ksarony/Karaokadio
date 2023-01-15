from django.shortcuts import redirect, render, HttpResponse
from .models import Station
from .forms import CreateStationForm


def index(request):
	user = request.user
	form = CreateStationForm()
	if request.method == "POST":
		form = CreateStationForm(request.POST)
		if form.is_valid():
			station = form.save(commit=False)
			station.created_by = user
			station.save()
			return redirect("station:index")
	stations = Station.objects.all()
	return render(request, 'station/stations.html', {'form': form, 'stations': stations})


def listen_station(request, id):
	station = Station.objects.get(pk=id)
	return HttpResponse(station.description)


def delete_station(request, id):
	station = Station.objects.get(pk=id)
	station.delete()
	return redirect("station:index")
