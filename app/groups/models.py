from django.db import models
from django.contrib.auth.validators import ASCIIUsernameValidator, UnicodeUsernameValidator
from django.utils import six, timezone
from django.utils.translation import ugettext_lazy as _


class Group(models.Model):
    GROUP_STATUS = (
        (0, 'Otwarta'),
        (1, 'Zamknięta'),
        # (2, 'Tajna'),
    )

    group_name_validator = UnicodeUsernameValidator() if six.PY3 else ASCIIUsernameValidator()

    group_name = models.CharField(
        _('Nazwa grupy'),
        max_length=150,
        unique=True,
        help_text=_('Maksymalna długość 150 znaków. Dozwolone są litery, cyfry i @/./+/-/_.'),
        validators=[group_name_validator],
        error_messages={
            'unique': _("Grupa o takiej nazwie już istnieje"),
            'invalid': _("Podaj poprawną nazwę grupy"),  # Override group_name_validator error
        },
    )

    group_description = models.CharField(
        _('Opis grupy'),
        max_length=300
    )

    group_status = models.IntegerField(
        _('Status grupy'),
        choices=GROUP_STATUS,
        default=0,
    )

    date_created = models.DateTimeField(
        _('Data utworzenia'),
        default=timezone.now,
    )


class Tag(models.Model):
    tag_name_validator = UnicodeUsernameValidator() if six.PY3 else ASCIIUsernameValidator()

    tag_name = models.CharField(
        _('Nazwa tagu'),
        max_length=50,
        unique=True,
        help_text=_('Maksymalna długość 50 znaków. Dozwolone są litery, cyfry i @/./+/-/_.'),
        validators=[tag_name_validator],
        error_messages={
            'unique': _("Tag o takiej nazwie już istnieje"),
            'invalid': _("Podaj poprawną nazwę tag"),  # Override group_name_validator error
        },
    )


class GroupTag(models.Model):
    group = models.ForeignKey(
        'Group',
        on_delete=models.CASCADE,
    )

    tag = models.ForeignKey(
        'Tag',
        on_delete=models.CASCADE,
    )

    class Meta:
        unique_together = ('group', 'tag',)


class UserGroup(models.Model):
    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
    )

    group = models.ForeignKey(
        'Group',
        on_delete=models.CASCADE,
    )

    USER_STATUS = (
        (0, 'Zwykły'),
        (1, 'Moderator'),
        (2, 'Administrator'),
    )

    user_status = models.IntegerField(
        _('Status użytkownika'),
        choices=USER_STATUS,
        default=0,
    )

    is_member = models.BooleanField(
        default=False
    )

    class Meta:
        unique_together = ('group', 'user',)
