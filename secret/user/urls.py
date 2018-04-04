from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    # user/image/
    url(r'^image/$', views.Image.as_view(), name='image'),
]