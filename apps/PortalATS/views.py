# from django.http import HttpResponse, HttpResponseRedirect
#
import os
from django.shortcuts import get_object_or_404, render

from django.http import HttpResponse
from django.shortcuts import redirect
import quicky

from . import models

from quicky import applications
from models import Login

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, load_backend, logout, login as form_login
import quicky

application = applications.get_app_by_file(__file__)
# from django.urls import reverse
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@quicky.view.template("index.html")
def index(request):
    if request.user.is_anonymous():
        return redirect(request.get_app_url("login"))
    else:
        model = {}
        return request.render(model)


def admin(request):
    return render(request, 'admin.html')


@quicky.view.template("login.html")
def login(request):
    try:
        sys_user = User.objects.get(username="sys")
    except ObjectDoesNotExist as ex:
        user = User.objects.create_user('sys', '', '123456')
        user.is_active = True
        user.is_supperuser = True
        user.save()
    _login = models.Login()
    _login.language = request._get_request().get("language", "en")
    if request.GET.has_key("next"):
        _login.url_next = request.GET["next"]
    request.session["language"] = _login.language
    if request._get_post().keys().__len__() > 0:
        username = request._get_post().get("username")
        password = request._get_post().get("password")
        try:
            ret = authenticate(username=request._get_post().get("username"),
                               password=request._get_post().get("password"))
            form_login(request, ret)
            return redirect(request.get_app_url(""))
        except Exception as ex:
            _login.is_error = True
            _login.error_message = request.get_global_res("Username or Password is incorrect")
            return request.render(_login)
    return request.render(_login)


def load_page(request, path):
    try:
        return request.render({})
    except:
        return HttpResponse("page was not found")


@quicky.view.template("sign_out.html")
def logout_view(request):
    logout(request, request.user.schema)
    # quicky.language.remove_language()
    request.session.clear()
    return redirect(request.get_app_url(""))


@quicky.view.template(is_public=True)
def change_language(request):
    import quicky
    from django.conf import settings as st
    lan = request.GET.get('language', st.LANGUAGE_CODE)
    request.session['language'] = lan
    quicky.language.set_language(lan)
    return redirect(request.get_app_url(""))


@quicky.view.template("sign_out.html")
def sign_out(request):
    membership.sign_out(request.session.session_key)
    request.session.clear()
    return redirect("/")


# @quicky.view.template("list.html")
# def load_list(request,path):
#    #form = getattr(forms, path)
#    return request.render({
#        "path": u"list/" + path.lower()
#    })

@quicky.view.template(
    file="dynamic.html",
    is_public=True
)
def load_page(request, path):
    return request.render({
        "path": path.lower()
    })


@quicky.view.template(is_public=True)
def file_download(request):
    from api import LMSLS_MaterialManagement as fnMaster
    id = request.REQUEST['id']
    if (id != None):
        data = fnMaster.get_file_by_master_id(str(id))
        if (data != None):
            import base64
            from django.http import HttpResponse
            from wsgiref.util import FileWrapper

            # generate the file
            res = HttpResponse(data["files"]["file_data"].split(',')[1].decode('base64'))
            res['Content-Type'] = data["files"]["file_type"]
            res['Content-Length'] = data["files"]["file_size"]
            res['Content-Disposition'] = 'attachment; filename=' + data["files"]["file_name"]
            return res
        # return response
    return request