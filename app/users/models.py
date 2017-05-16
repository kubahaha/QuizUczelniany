# -*- coding: utf-8 -*-
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.validators import ASCIIUsernameValidator, UnicodeUsernameValidator
from django.utils import six, timezone
from django.db import models
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import AbstractBaseUser


class UserManager(BaseUserManager):
    """
    Inherits methods: normalize_email, make_random_password, get_by_natural_key
    """
    def create_user(self, username, email, password):
        if not email:
            raise ValueError('Users must have an email address')  # TODO translate

        if not username:
            raise ValueError('The given username must be set')

        if not password:
            raise ValueError('Users must have an password')

        user = self.model(
            email=self.normalize_email(email),
            username=username
        )

        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    """
    Extends AbstractBaseUser, inherits password field and set of useful methods
    Added some fields and methods based on builtin django user (AbstractUser) class
    At the end contains: ID(default if no pk specified), username, email, password, date_joined, last_login
    """
    username_validator = UnicodeUsernameValidator() if six.PY3 else ASCIIUsernameValidator()

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Maksymalna długość 150 znaków. Dozwolone są litery, cyfry i @/./+/-/_.'),
        validators=[username_validator],
        error_messages={
            'unique': _("Użytkownik o takiej nazwie już istnieje"),
            'invalid': _("Podaj poprawną nazwę użytkownika"),  # Override username_validator error
        },
    )

    email = models.EmailField(
        _('email address'),
        unique=True,
        error_messages={
            'unique': _("Użytkownik o takim emailu już istnieje"),
        },
    )

    date_joined = models.DateTimeField(
        _('date joined'),
        default=timezone.now
    )

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'

    REQUIRED_FIELDS = ['password', 'email']

    def clean(self):
        super(User, self).clean()  # call base method - clearing username

    def get_full_name(self):
        """
        Base method force to override this method
        Just return username
        """
        return self.username

    def get_short_name(self):
        """
        Base method force to override this method
        Just return username
        """
        return self.username
