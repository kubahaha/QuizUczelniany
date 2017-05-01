from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import *


def welcome(request, register_form=None, login_form=None):
    if request.user.is_authenticated():
        return redirect('user:logged')

    if register_form is None:
        register_form = RegistrationForm()

    if login_form is None:
        login_form = LoginForm()

    return render(request, "not_logged_welcome.html", {'login_form': login_form, 'register_form': register_form})


def register(request):
    if request.user.is_authenticated():
        return redirect('user:logged')

    if request.method == "POST":
        form = RegistrationForm(request.POST)

        if form.is_valid():
            form.save()

            return render(request, "registered.html")

        return welcome(request, register_form=form)

    return redirect('user:welcome')


def login_page(request):
    if request.user.is_authenticated():
        return redirect('user:logged')

    if request.user.is_authenticated():
        redirect('user:logged')

    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            user = authenticate(login=form.cleaned_data['login'], password=form.cleaned_data['password'])
            login(request, user)

            return redirect("user:logged")

        return welcome(request, login_form=form)

    return redirect('user:welcome')


def logintest(request):
    return render(request, "logintest.html")
