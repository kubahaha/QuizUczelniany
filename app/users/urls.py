from django.conf.urls import url
from . import views

app_name = 'user'  # for template namespace

urlpatterns = [
    url(r'^dashboard/account/$', views.user_settings, name="user_settings"),
    url(r'^dashboard/account/changemail$', views.user_change_email, name="user_change_mail"),
    url(r'^dashboard/account/changepassword$', views.user_change_password, name="user_change_password"),
    url(r'^guest/$', views.welcome, name="welcome"),
    url(r'^guest/register/$', views.register, name="registration"),
    url(r'^guest/login/$', views.login_page, name="login"),
    url(r'^logout/$', views.logout_user, name="logout"),
]