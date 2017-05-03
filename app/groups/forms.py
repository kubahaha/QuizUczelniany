from django import forms
from django.forms import Textarea
from .models import Group, Tag
from django.contrib.auth.validators import ASCIIUsernameValidator, UnicodeUsernameValidator
from django.utils import six
from django.utils.translation import ugettext_lazy as _


class AddGroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ('group_name', 'group_status', 'group_description')

        widgets = {
            'group_description': Textarea(),
        }


class AddTags(forms.Form):
    tag_name_validator = UnicodeUsernameValidator() if six.PY3 else ASCIIUsernameValidator()

    def __init__(self, *args, **kwargs):
        super(AddTags, self).__init__(*args, **kwargs)

        # for i in range(10):
        #     tag_temp = fields_for_model(model=Tag, fields=('tag_name',))
        #     tag_temp['tag_name'].required = False
        #     tag_temp['tag_name_%s' % i] = tag_temp.pop('tag_name')
        #     self.fields.update(tag_temp)

        for i in range(10):
            tag_temp = forms.CharField(max_length=50,
                                       help_text=_(
                                           'Maksymalna długość 50 znaków. Dozwolone są litery, cyfry i @/./+/-/_.'),
                                       validators=[self.tag_name_validator],
                                       error_messages={
                                           'unique': _("Tag o takiej nazwie już istnieje"),
                                           'invalid': _("Podaj poprawną nazwę tag"),
                                       },
                                       required=False)
            self.fields.update({'tag_name_%s' % i: tag_temp})

    def save(self):
        name_list = []

        for key, value in self.cleaned_data.items():
            if value != '':
                tag, status = Tag.objects.get_or_create(tag_name=value)
                name_list.append(tag)

        return name_list
