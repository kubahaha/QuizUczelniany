# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from django.contrib.auth import authenticate
from .models import User


class RegistrationForm(ModelForm):
    """
    Can be inherit from builtin form https://github.com/django/django/blob/master/django/contrib/auth/forms.py#L64
    """
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'username')

    def clean(self):
        cleaned_data = super().clean()  # check db constrains and others stuff declared on model

        # if ('password1' not in cleaned_data) and ('password2' not in cleaned_data) \
        #         and cleaned_data['password1'] != cleaned_data['password2']:
        #     raise forms.ValidationError("Podane hasła nie są takie same!")

        if cleaned_data['password1'] != cleaned_data['password2']:
            raise forms.ValidationError("Podane hasła nie są takie same!")

        return cleaned_data

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.clean()

        if commit:
            user.save()

        return user

class LoginForm(forms.Form):
    login = forms.Field(widget=forms.TextInput)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()

        login = cleaned_data['login']
        password = cleaned_data['password']

        user = authenticate(login=login, password=password)
        if user is None:
            raise forms.ValidationError("Niepoprawne dane logowania")

        return cleaned_data



class ChangeUserPasswordForm(forms.Form):
    password1 = forms.Field(label='New Password', widget=forms.PasswordInput)
    password2 = forms.Field(label='Password confirmation', widget=forms.PasswordInput)
    current_password = forms.Field(label='Old Password', widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ChangeUserPasswordForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()

        if ('password1' not in cleaned_data) or ('password2' not in cleaned_data) \
                or cleaned_data['password1'] != cleaned_data['password2']:
            raise forms.ValidationError("Podane hasła nie są takie same!")

        if ('current_password' not in cleaned_data) or not self.user.check_password( cleaned_data['current_password'] ):
            raise forms.ValidationError("Podane hasło jest błędne!")

        return cleaned_data


class ChangeUserEmail(forms.Form):
    new_email = forms.EmailField(label='New Email')

    def clean(self):
        cleaned_data = super().clean()

        if User.objects.filter(email=cleaned_data['new_email']).exists():
            raise forms.ValidationError("Podany email już jest zarejestrowany!")

        return cleaned_data
