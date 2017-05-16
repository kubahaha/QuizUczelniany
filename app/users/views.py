# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import *


def welcome(request, register_form=None, login_form=None):
    if request.user.is_authenticated():
        return redirect('group:index')

    if register_form is None:
        register_form = RegistrationForm()

    if login_form is None:
        login_form = LoginForm()

    return render(request, "welcome.html", {'login_form': login_form, 'register_form': register_form})


def register(request):
    if request.user.is_authenticated():
        return redirect('group:index')

    if request.method == "POST":
        form = RegistrationForm(request.POST)

        if form.is_valid():
            form.save()

            return render(request, "registered.html")

        return welcome(request, register_form=form)

    return redirect('user:welcome')


def login_page(request):
    if request.user.is_authenticated():
        return redirect('group:index')

    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            user = authenticate(login=form.cleaned_data['login'], password=form.cleaned_data['password'])
            login(request, user)

            return redirect('group:index')

        return welcome(request, login_form=form)

    return redirect('user:welcome')


def logout_user(request):
    logout(request)

    return redirect('user:welcome')


def user_settings(request, password_change_form=None, email_change_form=None, context=''):
    if password_change_form is None:
        password_change_form = ChangeUserPasswordForm()

    if email_change_form is None:
        email_change_form = ChangeUserEmail()

    return render(request, "user_settings.html",
                  {'password_form': password_change_form, 'email_form': email_change_form, 'context': context})


def user_change_email(request):
    if request.method == "POST":
        email_change_form = ChangeUserEmail(request.POST)

        if email_change_form.is_valid():
            new_email = email_change_form.cleaned_data['new_email']
            request.user.email = new_email
            request.user.save()

            return user_settings(request, context="Udało się zmienić mejla!")

        return user_settings(request, email_change_form=email_change_form)

    return redirect('user:user_settings')


def user_change_password(request):
    if request.method == "POST":
        password_change_form = ChangeUserPasswordForm(request.POST, user=request.user)

        if password_change_form.is_valid():
            new_password = password_change_form.cleaned_data['password1']
            request.user.set_password(new_password)
            request.user.save()

            return user_settings(request, context="Udało się zmienić hasło!")

        return user_settings(request, password_change_form=password_change_form)

    return redirect('user:user_settings')
