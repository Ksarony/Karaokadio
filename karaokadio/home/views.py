from django.shortcuts import render, redirect
from django.contrib.auth import login as session_login, authenticate, logout as session_logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignupForm


def index(request):
	return render(request, 'home/landing.html')


def login(request):
	form = AuthenticationForm()
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			session_login(request, user)
			return redirect("/")
	return render(request=request, template_name="home/login.html", context={"login_form": form})


def signup(request):
	form = SignupForm()
	if request.method == "POST":
		form = SignupForm(request.POST)
		if form.is_valid():
			user = form.save()
			session_login(request, user)
			return redirect("/")
	return render(request=request, template_name="home/signup.html", context={"signup_form": form})


def logout(request):
	session_logout(request)
	return redirect("/")
