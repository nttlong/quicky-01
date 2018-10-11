# -*- coding: utf-8 -*-
from quicky import tenancy
from django.contrib.auth import authenticate, login as request_login
from django.shortcuts import redirect
from . import menu
import importlib
import json
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from quicky import layout_view
from quicky import authorize

import logging

import quicky
from quicky import dict_utils
logger = logging.getLogger(__name__)

application=quicky.applications.get_app_by_file(__file__)
logger = logging.getLogger(__name__)
@quicky.view.template("index.html")
def index(request):

    menu_items=[]
    return request.render(
        dict(
            menu_items=menu.menu_items
        )
    )
@quicky.view.template("category.html")
def load_categories(request,path):
    return {}
    # form =importlib.import_module("{0}.forms.{1}".format(application.name,path))# get declare form at forms package
    # config=form.layout.get_config() # get config of form
    # return request.render({
    #     "path": path.lower(),
    #     "columns":form.layout.get_table_columns(),
    #     "api_get_list":config.get("action_list","hrm.api.categories/get_list")
    # })
@quicky.view.template("category-editor.html")
def load_category(request,path):
    return {}
    # form = importlib.import_module("{0}.forms.{1}".format(application.name, path))
    # config = form.layout.get_config()
    # return request.render({
    #     "path": path.lower(),
    #     "form": form.layout.get_form(),
    #     "get_col": form.layout.get_form_col,
    #     "api_get_item": config.get("action_item", "hrm.api.categories/get_item"),
    #     "api_save_item": config.get("action_save_item", "hrm.api.categories/save_item"),
    #     "api_get_dictionary":config.get("action_get_distionary", "hrm.api.categories/get_dictionary"),
    #     "keys":config.get("keys", ["_id"]),
    # })
@quicky.view.template("dynamic.html")
def load_page(request,path):
    import os
    dir=os.path.dirname(application.mdl.__file__)
    html_file=dir+os.sep+"templates"+os.sep+"views"+os.sep+path+".html"
    html_file=html_file.replace('/',os.sep)
    if not os.path.isfile(html_file):
        f = open(html_file, 'w')
        f.write("<%inherit file=\"base.html\"/>\r<div>\r</div>")
        f.close()
    request.set_file_template("views/"+path+".html")
    return request.render({
        "path": path
    })
@quicky.view.template("dynamic.html")
def load_dialog(request,path):
    import os
    dir=os.path.dirname(application.mdl.__file__)
    html_file=dir+os.sep+"templates"+os.sep+"views"+os.sep+path+".html"
    html_file=html_file.replace('/',os.sep)
    if not os.path.isfile(html_file):
        f = open(html_file, 'w')
        f.write("<%inherit file=\"base.html\"/>\r<div>\r</div>")
        f.close()
    return request.render({
        "path": path.lower()
    })
@quicky.view.template("login.html")
def login(request):
    from django.contrib.auth.models import User
    try:
        sys_user=User.objects.get(username='sys',schema=tenancy.get_schema())
        sys_user.is_staff = True
        sys_user.is_superuser = True
        sys_user.save(schema=tenancy.get_schema())
    except Exception as ex:
        user = User.objects.create_user(username='sys',
                                        email='sys@beatles.com',
                                        password='123456',
                                        schema=tenancy.get_schema())
        user.is_staff = True
        user.is_superuser = True
        user.save(schema=tenancy.get_schema())
    _login = {
        "username":"",
        "password":"",
        "language":"en",
        "next":""
    }
    _login["language"] = request._get_request().get("language", "en")
    request.set_language(_login["language"])
    if dict_utils.has_key(request.GET,"next"):
        _login["next"] = request.GET.get("next",request.get_app_url(""))
    request.session["language"] = _login["language"]
    if request._get_post().keys().__len__() > 0:

        _login["username"] = request._get_post().get("username","")
        _login["password"] = request._get_post().get("password","")
        _login["language"] = request._get_post().get("language", "en")
        user=authenticate(username=request._get_post().get("username",""),
                          password=request._get_post().get("password",""),
                          schema=tenancy.get_schema())
        if user==None:
            _login.update(dict(
                error=dict(
                    message=request.get_global_res("Username or Password is incorrect")
                )
            ))
            return request.render(_login)
        else:
            request_login(request,user,schema=tenancy.get_schema())
            return redirect(_login["next"])


    return request.render(_login)
@quicky.view.template("sign_out.html")
def sign_out(request):
    from quicky.api import logout
    logout(request)
    return redirect(request.get_app_url(""))
@quicky.view.template("download_excel.html")
def download_excel(request,path):
    from .api import categories
    from quicky import tenancy
    from qexcel import export_excel
    coll =categories.get_coll(path)
    qr= coll().aggregate()
    ret = export_excel.do_export(request.get_language(), application.name, tenancy.get_schema(), coll()._model.name, qr)

    return ret