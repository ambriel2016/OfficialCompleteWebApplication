from django.contrib import auth
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm


# Create your views here.
def signup(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			raw_password = form.cleaned_data.get('password1')
			user = authenticate(username=username, password=raw_password)
			login(request, user)
			return redirect('dashboard')
	else:
		form = UserCreationForm()
		return render(request, 'accounts/signup.html', {'form': form})


def signin(request):
	return render(request, 'accounts/signin.html')


def logout(request):
	# TODO need to route to home page and don't forget to signout
	# and don't forget to signout
	return render(request, '')


def urlsinput(request):
	return render(request, 'accounts/urlsinput.html')


def output(request):
	return render(request, 'accounts/output.html')


def dashboard(request):
	return render(request, 'accounts/dashboard.html')
