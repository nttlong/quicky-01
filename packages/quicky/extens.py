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

    def register_view():
        return applications.get_settings().AUTHORIZATION_ENGINE.register_view(app=get_app_name(),view=get_view_path())
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
            "model": model,
            "request":request
        }
        for k,v in request.__fn__.items():
            try:
                render_model.update({k:v})
            except Exception as ex:
                print v
        render_model.update({"encryptor":encryptor})
        # mylookup = TemplateLookup(directories=config._default_settings["TEMPLATES_DIRS"])
        if fileName != None:
            ret_res=None
            mylookup = TemplateLookup(directories=[os.getcwd() + "/" + request.get_app().template_dir],
                                      default_filters=['decode.utf8'],
                                      input_encoding='utf-8',
                                      output_encoding='utf-8',
                                      encoding_errors='replace',

                                      )
            ret_res=mylookup.get_template(fileName).render(**render_model)
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
