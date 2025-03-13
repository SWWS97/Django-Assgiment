from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as django_login
from django.shortcuts import render, redirect
from django.http import Http404
from todo.models import Todo
from django.conf import settings
from django.urls import reverse


def todo_list(request):
    todo_list = Todo.objects.all().values_list('id', 'title')
    result = [{'id': todo[0], 'title': todo[1]} for i, todo in enumerate(todo_list)]

    return render(request, 'todo_list.html', {'data':result})


def todo_info(request, todo_id):
    try:
        todo = Todo.objects.get(id=todo_id)
        info = {
            'title': todo.title,
            'description': todo.description,
            'start_date': todo.start_date,
            'end_date': todo.end_date,
            'is_completed': todo.is_completed,
        }
        return render(request, 'todo_info.html', {'data': info})
    except Todo.DoesNotExist:
        raise Http404("Todo does not exist")



def signup(request):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect(settings.LOGIN_URL)

    context = {
        'form': form
    }

    return render(request, 'registration/sign.html', context)



def login(request):
    form = AuthenticationForm(request, request.POST or None)

    if form.is_valid():
        django_login(request, form.get_user())
        return redirect(reverse('todo_list'))

    context = {
        'form': form
    }

    return render(request, 'registration/login.html', context)
