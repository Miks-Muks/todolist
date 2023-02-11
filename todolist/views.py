from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from todolist.forms import ToDoForm
from .models import Todo
from django.utils import timezone


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
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('home')
            except IntegrityError:
                return render(request, 'todolist/signup user.html', {'form': UserCreationForm(),
                                                                     'error': 'That username has already been taken. '
                                                                              'Please choose a new username'})
        else:
            return render(request, 'todolist/signup user.html', {'form': UserCreationForm(),
                                                                 'error': 'Password not cool'})


def login_user(request):
    if request.method == 'GET':
        auth = AuthenticationForm()
        return render(request, 'todolist/login.html', context={'auth': auth})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'todolist/login.html',
                          {'form': AuthenticationForm(), 'error': 'Username and password did not match'})
        else:
            login(request, user)
            return redirect('current_to_do')


@login_required
def logout_user(request):
    if request.method == 'POST':
        logout(request)
        return redirect(to='home')


@login_required
def create_todo(request):
    if request.method == 'GET':
        todo_form = ToDoForm()
    else:
        try:
            todo_form = TodoForm(request.POST)
            newtodo = todo_form.save(commit=False)
            newtodo.user = request.user
            newtodo.save()
            return redirect('current_to_do')
        except ValueError:
            return render(request, 'todolist/create_todo.html',
                          {'form': TodoForm(), 'error': 'Bad data passed in. Try again.'})


@login_required
def current_to_do(request):
    todos = Todo.objects.filter(user=request.user, date_completed_isnull=True)
    return render(request, 'todolist/currenttodos.html', {'todos': todos})


@login_required
def complete_todo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.datecompleted = timezone.now()
        todo.save()
        return redirect('current_to_do')


@login_required
def create_to_do(request):
    if request.method == "GET":
        form_todo = ToDoForm()
        return render(request, 'todolist/create todo.html', {'form_todo': form_todo})
    elif request.method == 'POST':
        form = ToDoForm(request.POST)


@login_required
def completed_todos(request):
    todos = Todo.objects.filter(user=request.user, date_completed_isnull=False)
    return render(request, 'todolist/completed_todos.html', {'todos': todos})


@login_required
def delete_todo(request, todo_id):
    todo = get_object_or_404(Todo, pk=todo_id, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect(to='current_to_do')
