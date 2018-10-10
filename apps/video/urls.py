from django.conf.urls import include, url
from django.contrib import admin
from . import views
import quicky
app=quicky.applications.get_app_by_file(__file__)
from django.conf.urls.static import static
import os
app=quicky.applications.get_app_by_file(__file__)
urlpatterns = [
    url(r'^$/(?P<id>.*)$', views.index, name='index'),
    url(r'^$/upload', views.upload, name='upload'),
    url(r'^api$',"quicky.api.call"),
    app.get_static_urls()
]