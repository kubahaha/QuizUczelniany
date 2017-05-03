from django.db import transaction
from django.shortcuts import render
from .forms import *
from .models import *

def index(request):
    groups = Group.objects.all()
    groups_with_tags = {}
    count = 0
    for group in groups:
        group_id = group.id
        tags = Tag.objects.raw("SELECT T.id, tag_name FROM groups_tag AS T JOIN groups_grouptag AS GT on T.id = GT.tag_id WHERE GT.group_id = %s", [group_id])
        groups_with_tags[count] = {"Group": group, "Tags": tags}
        count = count + 1

    return render(request, "index.html", {'groups_with_tags': groups_with_tags})


def add_group(request):
    group_form = AddGroupForm(request.POST or None)
    tag_form = AddTags(request.POST or None)

    if group_form.is_valid() and tag_form.is_valid():
        with transaction.atomic():
            group = group_form.save()
            tags = tag_form.save()

            for tag in tags:
                GroupTag.objects.get_or_create(group=group, tag=tag)

        return render(request, "successfully_added_group.html")

    return render(request,
                  "add_group.html",
                  {'add_group_form': group_form,
                   'tag_form': tag_form})
