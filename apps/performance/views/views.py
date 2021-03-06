import os
import qmongo
from django.shortcuts import get_object_or_404, render

from django.http import HttpResponse
from django.shortcuts import redirect
import quicky

from .. import LoginModel

from quicky import applications

from .. api.models import auth_user_info
from django.contrib.auth import authenticate, load_backend, logout, login as form_login
import quicky
application=applications.get_app_by_file(__file__)
# from django.urls import reverse
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

@quicky.view.template("index.html")
def index(request):
    
    if request.user.is_anonymous():
        if hasattr(quicky.system_settings, "SSO_LOGIN_URL") and quicky.system_settings.SSO_LOGIN_URL != "":
            return redirect(quicky.system_settings.SSO_LOGIN_URL + "?ret=" + request.get_app_url(""))
        return redirect(request.get_app_url("login"))
    else:
        model = {}
        return request.render(model)

def admin(request):
    return render(request, 'admin.html')

@quicky.view.template("login.html")
def login(request):
    #try:
    #    sys_user=User.objects.get(username="sys")
    #except ObjectDoesNotExist as ex:
    #    user = User.objects.create_user('sys', '', '123456')
    #    user.is_active=True
    #    user.is_supperuser=True
    #    user.save()
    _login=LoginModel.Login()
    #from django.conf import settings as st
    import SystemConfig
    st = SystemConfig.get()
    _login.language=request._get_request().get("language", st.default_language)
    if request.GET.has_key("next"):
        _login.url_next=request.GET["next"]
        if request._get_post().get("site") != None and request._get_post().get("site") != "":
            _login.url_next= request.GET["next"] + request._get_post().get("site")
    if request._get_post().keys().__len__()>0:
        username_request=request._get_post().get("username")
        password_request=request._get_post().get("password")
        try:
            from quicky import tenancy

            user_login =qmongo.models.auth_user_info.aggregate.project(username=1, login_account=1)\
                .match("login_account == @account", account = username_request).get_item()
            if user_login==None:
                raise (Exception("User was not found"))

            ret=authenticate(username=user_login['username'], password=password_request,schema=tenancy.get_schema())
            if ret.backend != quicky.applications.get_settings().AUTHENTICATION_BACKENDS[0]:
                raise(Exception("user backend not correctly"))

            form_login(request,ret,schema=tenancy.get_schema())
            from quicky import language
            language.set_language(_login.language)
            request.session["language"] = _login.language
            return redirect(request.get_app_url(request._get_post().get("site")))
        except Exception as ex:
            _login.is_error=True
            _login.error_message=request.get_global_res("Username or Password is incorrect")
            return request.render(_login)
    if hasattr(quicky.system_settings, "SSO_LOGIN_URL") and quicky.system_settings.SSO_LOGIN_URL != "":
        return redirect(quicky.system_settings.SSO_LOGIN_URL + "?ret=" + request.get_app_url(""))
    return request.render(_login)

def load_page(request,path):
    try:
        return request.render({})
    except:
        return HttpResponse("page was not found")

@quicky.view.template("sign_out.html")
def logout_view(request):
    import SystemConfig
    logout(request, request.user.schema)
    #quicky.language.remove_language()
    SystemConfig.clear_cache()
    request.session.clear()
    if hasattr(quicky.system_settings, "LOGOUT_URL") and quicky.system_settings.LOGOUT_URL != "":
        return redirect(quicky.system_settings.LOGOUT_URL)
    else:
        return redirect(request.get_app_url(""))

@quicky.view.template(is_public=True)
def change_language(request):
    import quicky
    from django.conf import settings as st
    lan = request.GET.get('language', st.LANGUAGE_CODE)
    request.session['language'] = lan
    quicky.language.set_language(lan)
    return redirect(request.get_app_url(""))

@quicky.view.template("unauthorized.html")
def unauthorized(request):
    return request.render({
        "path":"unauthorized"
    })

#@quicky.view.template("list.html")
#def load_list(request,path):
#    #form = getattr(forms, path)
#    return request.render({
#        "path": u"list/" + path.lower()
#    })

@quicky.view.template(
    file="dynamic.html",
    is_public=True
)
def load_page(request,path):
    #Lam on duong sua cho nay, neu sua kg chay duoc tren linux nhe
    request.set_file_template("views/" + path + ".html")
    return  request.render({
        "path":path
    })
