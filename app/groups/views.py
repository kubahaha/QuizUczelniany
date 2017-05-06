from django.db import transaction
from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.db.models import Q


def index(request):
    groups_with_tags = associate_tags_with_given_groups()

    return render(request, "index.html", {'groups_with_tags': groups_with_tags})


def add_group(request):
    group_form = AddGroupForm(request.POST or None)
    tag_form = AddTags(request.POST or None)

    if group_form.is_valid() and tag_form.is_valid():
        with transaction.atomic():
            group = group_form.save()
            UserGroup.objects.create(user=request.user, group=group, user_status=2, is_member=True)
            tags = tag_form.save()

            for tag in tags:
                GroupTag.objects.get_or_create(group=group, tag=tag)

        return render(request, "successfully_added_group.html")

    return render(request,
                  "add_group.html",
                  {'add_group_form': group_form,
                   'tag_form': tag_form})


def search_groups(request):  # TODO via POST method
    # gets all search tag names only from input fields starts with 't' and ends with digit (max 10)
    request_tag_list = list(v for k, v in request.GET.items() if k[0] == 't' and len(k) == 2 and k[1].isdigit())

    groups_with_tags = {}
    tag_list = {}

    if request.method == "GET":
        search_query = request.GET.get('q')
        # no searching
        if (search_query == '' or search_query is None) and not request_tag_list:
            groups_with_tags = associate_tags_with_given_groups()
        # searching without selected tags
        elif search_query != '' and not request_tag_list:
            groups = Group.objects.filter(Q(group_name__contains=search_query) | Q(group_description__contains=search_query))
            groups_with_tags = associate_tags_with_given_groups(groups=groups)
        # searching with tags and with or without q
        else:
            groups = get_groups_which_have_given_tags_name_descript(request_tag_list, search_query)
            groups_with_tags = associate_tags_with_given_groups(groups=groups)

        tag_list = Tag.objects.all()

    return render(request, "search_groups.html", {'groups_with_tags': groups_with_tags, 'tags': tag_list})


# TODO add to context questions etc
def enter_into_group(request, group_id):
    group = Group.objects.filter(id=group_id).first()
    group_with_tags = associate_tags_with_given_groups([group])[0]
    print(group_with_tags)
    user_group_details = get_user_group_details(request.user.id, group_id)
    print(user_group_details)

    if not user_group_details['is_in_group'] or not user_group_details['is_member']:
        return render(request, 'not_a_member.html',
                      {'group_with_tags': group_with_tags, 'user_group_details': user_group_details})

    if user_group_details['is_member']:
        return render(request, 'group_index.html',
                      {'group_with_tags': group_with_tags, 'user_group_details': user_group_details})


def become_member(request, group_id):
    # user is already member of this group or request is not POST
    if request.method != "POST" or is_user_group_member(request.user.id, group_id):
        return redirect('group:go_to_group', group_id)

    # user is not member of this group
    group = Group.objects.filter(id=group_id).first()
    group_status = group.group_status

    if group_status == 0:  # group is open
        UserGroup.objects.create(user=request.user, group=group, user_status=0, is_member=True)
    else:  # group is closed
        UserGroup.objects.create(user=request.user, group=group, user_status=0, is_member=False)

    return redirect('group:go_to_group', group_id)


def group_admin(request):  # TODO
    pass


########
# UTILS
########
def is_user_group_member(user_id, group_id):
    return UserGroup.objects.filter(user_id=user_id, group_id=group_id).exists()
