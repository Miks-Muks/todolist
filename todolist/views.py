from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


# Create your views here.


def home(requests):
    return render(requests, 'todolist/home.html')


def sighup(request):
    if request.method == 'GET':
        form = UserCreationForm
        return render(request, 'todolist/sighup user.html', {'form': form})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('home')
            except IntegrityError:
                return render(request, 'todolist/signup user.html', {'form': UserCreationForm(),
                                                                     'error': 'That username has already been taken. '
                                                                              'Please choose a new username'})


def login(request):
    if request.method == 'GET':
        auth = AuthenticationForm
        return render(request, 'todolist/login.html', context={'auth': auth})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])


def current_to_do(request):
    pass
