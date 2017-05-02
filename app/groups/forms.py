from django import forms
from django.forms import Textarea
from .models import Group


class AddGroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ('group_name', 'group_status', 'group_description')

        widgets = {
            'group_description': Textarea(),
        }

    # TODO validation and save

