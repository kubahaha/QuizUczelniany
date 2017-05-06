from django.db import models
from django.contrib.auth.validators import ASCIIUsernameValidator, UnicodeUsernameValidator
from django.utils import six, timezone
from django.utils.translation import ugettext_lazy as _


class GroupNameValidator(UnicodeUsernameValidator):
    """
    Just overwritten UsernameValidator regexp, now it allows for spaces
    Spaces can't be put at the beginning and at the end nor more than one in a row
    """
    regex = r'^[.\w.@+-]+([ .]{1}[\w.@+-]+)*$'


class Group(models.Model):
    GROUP_STATUS = (
        (0, 'Otwarta'),
        (1, 'Zamknięta'),
        # (2, 'Tajna'),
    )

    group_name_validator = GroupNameValidator()

    group_name = models.CharField(
        _('Nazwa grupy'),
        max_length=150,
        unique=True,
        help_text=_('Maksymalna długość 150 znaków. Dozwolone są litery, cyfry, spacje i @/./+/-/_.'
                    'Spacje nie mogą być na początku u na końcu nazwy, oraz nie może być więcej niż jedna pod rząd'),
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


# TODO: order by
def associate_tags_with_given_groups(groups=None, tag_list=None):
    """
    Gets valid Group instance or none,
    If Group is None then gets all existing groups
    Returns dict: {#id0: {'Group': GroupObject, 'Tags': TagObjectSet}, #id1: ... }, #id is order number
    """
    if groups is None:
        # get all groups
        groups = Group.objects.all()

    groups_with_tags = {}
    count = 0
    for group in groups:
        group_id = group.id  # TODO: cursor.fetchall()/dictfetchall(cursor) ?
        tags = Tag.objects.raw(
            "SELECT T.id, tag_name FROM groups_tag AS T JOIN groups_grouptag AS GT ON T.id = GT.tag_id WHERE GT.group_id = %s",
            [group_id])
        groups_with_tags[count] = {"Group": group, "Tags": tags}
        count = count + 1

    return groups_with_tags


def get_groups_which_have_given_tags_name_descript(tags, q_search):
    if tags is None:
        raise Exception('tags must be array!')

    if q_search is None:
        q_search = ''

    q_search = '%' + q_search + '%'

    groups = Group.objects.raw(
        '''SELECT DISTINCT ON (G.group_name) G.* FROM groups_group as G
            LEFT OUTER JOIN groups_grouptag as GT on G.id = GT.group_id
            LEFT OUTER JOIN groups_tag as T on T.id = GT.tag_id
              WHERE T.tag_name = ANY(%s)
                AND (G.group_name LIKE %s OR G.group_description LIKE %s)''',
        [tags, q_search, q_search]
    )

    return groups


def get_user_group_details(user_id, group_id):
    return_dict = {}

    user_details = UserGroup.objects.filter(user_id=user_id, group_id=group_id).first()

    if user_details is None:
        # if user is not in this group
        return_dict['is_in_group'] = False
        return return_dict

    return_dict['is_in_group'] = True
    return_dict['is_member'] = user_details.is_member
    return_dict['user_status'] = user_details.user_status

    return return_dict

