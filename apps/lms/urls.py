
from django.conf.urls import include, url
from django.contrib import admin
from . import views, excel
from excel import export
import quicky
app=quicky.applications.get_app_by_file(__file__)
from django.conf.urls.static import static
import os
app=quicky.applications.get_app_by_file(__file__)
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login$',views.login,name='logn'),
    url(r'^pages/(?P<path>.*)$', views.load_page, name='singleshop'),
    #url(r'^list/(?P<path>.*)$', views.load_list, name='singleshop'),
    url(r'^logout',views.logout_view),
    url(r'^language',views.change_language),
    url(r'^api$',"quicky.api.call"),
    url(r'^excel_export$', export.call, name='excel_export'),
    url(r'^get_schema', views.get_schema_main),
    app.get_static_urls()
]

