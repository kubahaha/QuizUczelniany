from django.shortcuts import render
from django.forms import modelformset_factory
from .forms import *
from .models import *


def index(request):
    groups = Group.objects.all().exclude()

    return render(request, "index.html", {'groups': groups})


def add_group(request):
    group_form = AddGroupForm()
    tag_formset = modelformset_factory(Tag, fields=('tag_name',))
    tag_form = tag_formset()

    return render(request, "add_group.html",
                  {'add_group_form': group_form,
                   'tag_form': tag_form})
