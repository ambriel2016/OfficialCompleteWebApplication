from django.contrib import auth
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, urls
from django.contrib.auth.forms import UserCreationForm


# Create your views here.
def register(request):
	if request.method=='POST':
		form = UserCreationForm(request.POST)

	# 	form.save creates the new user
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate(username=username, password=password)
			login(request, user)
			return redirect('index')
	else:
		form = UserCreationForm()

	context = {'form': form}
	return render(request, 'registration/register.html', context)


def logout(request):
	return render(request, 'registration/login.html')


def urlsinput(request):
	return render(request, 'accounts/urlsinput.html')


def output(request):
	return render(request, 'accounts/output.html')


def dashboard(request):
	return render(request, 'accounts/dashboard.html')

def index(request):
	return render(request, 'accounts/index.html')
