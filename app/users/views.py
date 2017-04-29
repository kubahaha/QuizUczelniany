from django.shortcuts import render
from django.contrib.auth import login
from .forms import *


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)

        if form.is_valid():
            form.save()

            return render(request, "registered.html")
    else:
        form = RegistrationForm()
        return render(request, "registration_form.html", {'form': form})

    return render(request, "registration_form.html", {'form': form})


def login_page(request):
    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            user = authenticate(login=form.cleaned_data['login'], password=form.cleaned_data['password'])
            login(request, user)

            return render(request, "logged.html")

        return render(request, "login.html", {'form': form})
    else:
        form = LoginForm()
        return render(request, "login.html", {'form': form})
