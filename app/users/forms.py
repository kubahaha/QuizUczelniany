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
    login = forms.Field(label='login', widget=forms.TextInput)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()

        login = cleaned_data['login']
        password = cleaned_data['password']

        user = authenticate(login=login, password=password)
        if user is None:
            raise forms.ValidationError("Niepoprawne dane logowania")

        return cleaned_data
