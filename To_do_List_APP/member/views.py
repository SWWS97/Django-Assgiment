from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import redirect, render
from django.urls import reverse
from django.conf import settings

def signup(request):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect(settings.LOGIN_URL)

    context = {
        'form': form
    }

    return render(request, 'registration/sign.html', context)



def login(request, django_login=None):
    form = AuthenticationForm(request, request.POST or None)

    if form.is_valid():
        django_login(request, form.get_user())
        return redirect(reverse('todo:list'))

    context = {
        'form': form
    }

    return render(request, 'registration/login.html', context)

