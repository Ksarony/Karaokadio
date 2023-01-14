from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return render(request, 'home/landing.html', {'a': 1000})


def laugh(request):
    return HttpResponse("Hello, world. Haha.")
