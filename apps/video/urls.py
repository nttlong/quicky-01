
from django.conf.urls import include, url
from django.contrib import admin
import quicky
app=quicky.applications.get_app_by_file(__file__)
from django.conf.urls.static import static
import os
app=quicky.applications.get_app_by_file(__file__)
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^api$',"quicky.api.call"),
    app.get_static_urls()
]
