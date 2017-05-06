from django.conf.urls import url
from . import views

app_name = 'group'  # for template namespace

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^search/$', views.search_groups, name="search_groups"),
    url(r'^addgroup/$', views.add_group, name="add_group"),
    url(r'^group/(?P<group_id>[0-9]+)/$', views.enter_into_group, name="add_group"),
]