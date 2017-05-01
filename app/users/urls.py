from django.conf.urls import url
from . import views

app_name = 'user'  # for template namespace

urlpatterns = [
    url(r'^guest/$', views.welcome, name="welcome"),
    url(r'^guest/register/$', views.register, name="registration"),
    url(r'^guest/login/$', views.login_page, name="login"),
    url(r'^$', views.logintest, name="logged"),
]