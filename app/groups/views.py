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


def search_groups(request):
    request_tag_list = get_searching_tags(request.GET)

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
    user_group_details = get_user_group_details(request.user.id, group_id)

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


def group_admin(request, group_id):  # TODO questions and quizzes
    """
    If user is not a member or is a normal user then redirect to group index
    else returns user_group_details, group_with_tags, group_members
    VIEW HAVE TO manage which content display admin and super admin
    """
    user_group_details = get_user_group_details(request.user.id, group_id)

    if not user_group_details['is_in_group'] or user_group_details['user_status'] == 0:
        # if is not a member or is a normal member
        return redirect('group:go_to_group', group_id)

    group = Group.objects.filter(id=group_id).first()
    group_with_tags = associate_tags_with_given_groups([group])[0]

    group_members = get_group_member(group_id)
    
    context = {'group_with_tags': group_with_tags,
               'user_group_details': user_group_details,
               'group_members': group_members}

    return render(request, "group_admin_panel.html", context=context)


def user_dashboard_group(request):
    user_group = Group.objects.filter(usergroup__user_id=request.user.id)
    user_group_details = associate_tags_with_given_groups(user_group)

    return render(request, "user_groups.html", {'user_group_details': user_group_details})


def user_dashboard_group_search(request):
    request_tag_list = get_searching_tags(request.GET)

    user_group_details = {}
    tag_list = {}

    if request.method == "GET":
        search_query = request.GET.get('q')
        # no searching
        if (search_query == '' or search_query is None) and not request_tag_list:
            user_group = Group.objects.filter(usergroup__user_id=request.user.id)
            user_group_details = associate_tags_with_given_groups(user_group)
        # searching without selected tags
        elif search_query != '' and not request_tag_list:
            user_group = Group.objects.filter(
                Q(usergroup__user_id=request.user.id),
                Q(group_name__contains=search_query) | Q(group_description__contains=search_query))
            user_group_details = associate_tags_with_given_groups(groups=user_group)
        # searching with tags and with or without q
        else:
            user_group = get_groups_which_have_given_tags_name_descript(request_tag_list, search_query, user_id=request.user.id)
            user_group_details = associate_tags_with_given_groups(groups=user_group)

        tag_list = Tag.objects.filter()

    return render(request, "search_groups.html", {'groups_with_tags': user_group_details, 'tags': tag_list})


########
# UTILS
########
def is_user_group_member(user_id, group_id):
    return UserGroup.objects.filter(user_id=user_id, group_id=group_id).exists()


def get_user_role(user_id, group_id):
    user = UserGroup.objects.filter(user_id=user_id, group_id=group_id, is_member=True).first()

    if user is None:
        return None

    return user.user_status


def get_searching_tags(request_method):
    """
    Returns all search tag names only from input fields starts with 't' and ends with digit (max 10)
    Gets request method - e.g. request.POST or request.GET
    """
    return list(v for k, v in request_method.items() if k[0] == 't' and len(k) == 2 and k[1].isdigit())
