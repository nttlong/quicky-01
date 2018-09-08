"""
This module support extent django http request
"""
import  os
import json
from . import applications
from . import encryptor
import sys
from django.http import HttpResponse
from mako.template import Template
from mako.lookup import TemplateLookup
from . import language as lang_manager
import threading
from . import tenancy
import logging
logger=logging.getLogger(__name__)
global lock
settings=None
_abs_urls ={}
lock=threading.Lock()
from datetime import date, datetime

from bson.objectid import ObjectId
import importlib
from . import applications
from . import dict_utils
_language_cache={}
_static_cache ={}
class render_server():
    def __init__(self):
        pass

def apply(request,template_file,app):
    """
    Apply request
    :param request:
    :param template_file:
    :param app:
    :return:
    """


    def get_app_url(path):
        return request.get_app_url(path)
    def get_app_host():
        return request.get_app_host()
    def get_view_path():
        return request.get_view_path()






    def get_user():
        return request.user
    def get_res(key,value=None):
        return request.get_res(key,value)
    def get_app_res(key,value=None):
        return request.get_app_res(key,value)
    def get_global_res(key,value=None):
        return request.get_global_res(key,value)
    def get_static(path):
        return request.get_static(path)
    def get_abs_url():
        return request.get_abs_url()
    def get_app():
        return request.get_app()
    def get_app_name():
        return request.get_app_name()
    def get_api_key(path):
        return request.get_api_key(path)
    def get_api_path(id):
        return request.get_api_path()
    def register_view():
        return applications.get_settings().AUTHORIZATION_ENGINE.register_view(app=get_app_name(),view=get_view_path())
    def get_languages():
        return request.get_languages()

    def get_language_name():
        request.get_language_name()

    def get_language():
        return request.get_language()
    def set_language(lan):
        request.set_language(lan)
    def get_csrftoken():
        return request.get_csrftoken()

    def render(model):
        from mako import exceptions
        login_page=None
        is_public=None
        if type(template_file) is dict:
            fileName=template_file["file"]
            login_page=template_file.get("login",None)
            is_public = template_file.get("is_public", False)
        else:
            fileName = template_file


        render_model = {
            "get_res": get_res,
            "get_app_res": get_app_res,
            "get_global_res": get_global_res,
            "get_static": get_static,
            "get_abs_url": get_abs_url,
            "get_csrftoken": get_csrftoken,
            "model": model,
            "get_view_path": get_view_path,
            "get_user": get_user,
            "get_app_url": get_app_url,
            "get_app_host": get_app_host,
            "get_static": get_static,
            "get_language": get_language,
            "template_file": template_file,
            "get_api_key":get_api_key,
            "get_api_path":get_api_path,
            "register_view":register_view,
            "request":request,
            "encryptor":encryptor,
            "set_language":set_language,


        }
        # mylookup = TemplateLookup(directories=config._default_settings["TEMPLATES_DIRS"])
        if fileName != None:
            ret_res=None
            mylookup = TemplateLookup(directories=[os.getcwd() + "/" + request.get_app().template_dir],
                                      default_filters=['decode.utf8'],
                                      input_encoding='utf-8',
                                      output_encoding='utf-8',
                                      encoding_errors='replace',

                                      )
            # try:
            ret_res=mylookup.get_template(fileName).render(**render_model)

            # except exceptions.MakoException as ex:
            #     logger.debug(ex)
            #     raise (ex)
            # except Exception as ex:
            #     logger.debug(ex)
            #     logger.debug(exceptions.html_error_template().render())
            #     raise (Exception(exceptions.html_error_template().render()))
            return HttpResponse(ret_res)


        else:
            mylookup = TemplateLookup(directories=["apps/templates"],
                                      default_filters=['decode.utf8'],
                                      input_encoding='utf-8',
                                      output_encoding='utf-8',
                                      encoding_errors='replace'
                                      )
            return HttpResponse(mylookup.get_template(fileName).render(**render_model))

    # setattr(request,"template_file",template_file)
    setattr(request, "render", render)
    # setattr(request, "get_user", get_user)
    # setattr(request, "get_res", get_res)
    # setattr(request, "get_app_res", get_app_res)
    # setattr(request, "get_global_res", get_global_res)
    # setattr(request, "get_static", get_static)
    #
    # setattr(request, "get_app", get_app)
    # setattr(request,"get_view_path",get_view_path)
    # setattr(request,"get_app_host",get_app_host)
    # setattr(request, "get_app_url", get_app_url)
    #
    # setattr(request, "get_app_name", get_app_name)
    # setattr(request, "get_api_key", get_api_key)
    # setattr(request, "get_api_path", get_api_path)
    # setattr(request,"register_view",register_view)





