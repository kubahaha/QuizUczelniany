from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^register/$', views.register, name="registration"),
    url(r'^login/$', views.login_page, name="login"),
    url(r'^logintest/$', views.logintest, name="login"),
]