from django.conf.urls import include, url
from django.contrib import admin
from . import views
import quicky
from django.conf.urls.static import static
import os
app=quicky.applications.get_app_by_file(__file__)
urlpatterns = [
    url(r'^$', views.index, name='index'),
    # url(r'^login$',views.login,name='logn'),
    url(r'^pages/(?P<path>.*)$', views.load_page, name='singleshop'),
    url(r'^dialogs/(?P<path>.*)$', views.load_dialog, name='singleshop'),
    url(r'^categories/(?P<path>.*)$', views.load_categories, name='singleshop'),
    # url(r'^(?i)category/(?P<path>.*)$', views.load_category),
    url(r'^api$', "quicky.api.call"),
    url(r'^login$',views.login,name='logn'),
    app.get_static_urls(),
    url(r'^logout$',views.sign_out),
    url(r'^download/excel/(?P<path>.*)$',views.download_excel,name="download_excel")
]

