from django.db import transaction
from django.shortcuts import render
from .forms import *
from .models import *


def index(request):
    groups = Group.objects.all().exclude()

    return render(request, "index.html", {'groups': groups})


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
