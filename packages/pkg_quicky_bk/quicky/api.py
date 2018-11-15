"""
This module create api http request handler
"""
from . import tenancy
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import uuid
from django.http import HttpResponse
from . import dict_utils
import json
import importlib
import logging
from . import view as view_template
from . import JSON
from . import applications
import sys
import threading
import pymongo
from pymongo import MongoClient
from . layout_view import view
import re
global lock
lock = threading.Lock()
logger = logging.getLogger(__name__)
_cache_id={}
_cache_id_revert={}
_coll=None

class unauthorize(Exception):
    pass
class privilege_object():
    _param = None
    def __init__(self,param):
        self._param=param
    @property
    def is_full(self):
        if self._param == None:
            raise (unauthorize)
        return self._param.get("isFull",False)
    @property
    def is_allow_update(self):
        if self._param == None:
            raise (unauthorize)
        return self._param.get("allowUpdate", False) or self._param.get("isFull",False)
    @property
    def is_allow_insert(self):
        if self._param == None:
            raise (unauthorize)
        return self._param.get("allowInsert", False) or self._param.get("isFull",False)
    @property
    def is_allow_delete(self):
        if self._param == None:
            raise (unauthorize)
        return self._param.get("allowDelete", False) or self._param.get("isFull",False)
    @property
    def is_allow_select(self):
        if self._param == None:
            raise (unauthorize)
        return True


def check_privileges(args):
    if args["privileges"] == None:
        raise (unauthorize)


@require_http_methods(["POST","GET"])
@csrf_exempt
@view_template.template("call_api.html")
def call(request,*args,**kwargs):
    """
    Call request handler
    :param request:
    :return:
    """
    try:
        user = request.user
        #if user.is_anonymous():
        #    return HttpResponse('401 Unauthorized', status=401)
        #if not user.is_staff and not user.is_superuser:
        #    return HttpResponse('401 Unauthorized', status=401)
        post_data = JSON.from_json(request.body)
        if not dict_utils.has_key(post_data,"path"):
            raise Exception("Api post without using path")
        path = post_data["path"]
        view = post_data["view"]
        if not dict_utils.has_key(post_data,"offset_minutes"):
            raise (Exception("It look like you forget post 'offset_minutes' from client."
                             "Remember that before ajax post please set 'offset_minutes' from browser."
                             "How to calculate 'offset_minutes'?:"
                             "var now = new Date();"
                             "var offset_minutes = now.getTimezoneOffset();"))
        offset_minutes=post_data["offset_minutes"]
        setattr(threading.current_thread(),"client_offset_minutes",offset_minutes)
        setattr(threading.currentThread(),"client_offset_minutes",offset_minutes)


        path = get_api_path(path)

        get_privileges_of_user=applications.get_settings().AUTHORIZATION_ENGINE.get_privileges_of_user
        privilege=privilege_object(
            get_privileges_of_user(
                username=user.username,
                app=request.get_app().name,
                view=post_data["view"],
                schema=tenancy.get_schema()
                )
        )
        if user.is_superuser:
            view_privileges = {"is_public": True}
        method_path = path.split("/")[path.split("/").__len__() - 1]
        module_path = path[0:path.__len__() - method_path.__len__()-1]
        mdl = None
        try:
            mdl = importlib.import_module(module_path.replace("/","."))
        except unauthorize as ex:
            return HttpResponse('Unauthorized', status=401)
        except Exception as ex:
            logger.debug(ex)
            raise (ex)

        except ImportError as ex:
            logger.debug(Exception("import {0} is error or not found".format(module_path)))
            logger.debug(ex)
            raise Exception("import {0} is error or not found.Error description {1}".format(module_path,ex.message))

        except Exception as ex:
            if type(ex) is str:
                raise Exception("import '{0}' encountered '{1}'".format(module_path, ex))
            elif hasattr(ex,"messagte"):
                raise Exception("import '{0}' encountered '{1}'".format(module_path, ex))
            else:
                raise Exception("import '{0}' encountered '{1}'".format(module_path, ex))

        ret = None

        if mdl != None:
            try:
                if dict_utils.has_key(post_data,"data"):
                    ret = getattr(mdl, method_path)(
                        {
                            "privileges": privilege,
                            "data": post_data.get("data", {}),
                            "user": user,
                            "request": request,
                            "view":view
                        })
                else:
                    ret = getattr(mdl, method_path)(
                        {
                            "privileges": privilege,
                            "data": {},
                            "user": user,
                            "request": request,
                            "view":view
                        })

            except unauthorize as ex:
                return HttpResponse('Unauthorized', status=401)
            except Exception as ex:
                raise Exception("Call  '{0}' in '{1}' encountered '{2}'".format(method_path, module_path, ex))
        from django.http.response import HttpResponseRedirect
        if type(ret)== HttpResponseRedirect:

            return ret
        else:
            ret_data = JSON.to_json(ret)

        return HttpResponse(ret_data)
    except Exception as ex:
        logger.debug(ex)
        raise ex
def connect(*args,**kwargs):
    """

    """
    try:
        global _coll
        if args.__len__()==0:
            args=kwargs
        else:
            args=args[0]
        cnn = MongoClient(
            host=args["host"],
            port=args["port"]
        )
        db = cnn.get_database(args["name"])
        if args["user"] != "":
            db.authenticate(args["user"], args["password"])
            _coll=db.get_collection(args["collection"])

    except Exception as ex:
        logger.debug(ex)
        raise ex

def load_from_django_settings():
    from django.conf import settings
    connect(dict(
        host=settings.DATABASES["default"]["HOST"],
        port=settings.DATABASES["default"]["PORT"],
        user=settings.DATABASES["default"]["USER"],
        password=settings.DATABASES["default"]["PASSWORD"],
        name=settings.DATABASES["default"]["NAME"],
        collection="sys.api_caching"
    ))
def get_api_key(path):
    global _cache_id
    global _cache_id_revert
    global _coll
    if _coll==None:
        from django.conf import settings
        load_from_django_settings()
        if _coll == None:
            raise (Exception("It look like you forgot call api.connect on settings.py\n"
                             "\t\tHow to use this?:\n"
                             "\t\t\tIn settings.py:\n"
                             "\t\t\t\t\t  from quicky import api\n"
                             "\t\t\t\t\t  api.connect(\n"
                             "\t\t\t\t\t  host=db host,\n"
                             "\t\t\t\t\t  port= db port,\n"
                             "\t\t\t\t\t  name=db name,\n"
                             "\t\t\t\t\t  user=db user name,\n"
                             "\t\t\t\t\t  password=db password,\n"
                             "\t\t\t\t\t  collection=the name of collection storage api)\n"
                             ))
    if not dict_utils.has_key(_cache_id,path):
        lock.acquire()
        try:
            item=_coll.find_one({
                "api_path":{
                    "$regex":re.compile("^"+path+"$",re.IGNORECASE),
                }
            })
            if item==None:

                id = uuid.uuid4().__str__()
                _coll.insert_one({
                    "api_path":path,
                    "api_id":id
                })
                _cache_id.update({
                    path: id
                })
                _cache_id_revert.update({
                    id: path
                })
            else:
                id=item["api_id"]
                _cache_id.update({
                    path: item["api_id"]
                })
                _cache_id_revert.update({
                    id: item["api_path"]
                })

            lock.release()

        except Exception as ex:
            lock.release()
            logger.debug(ex)
            raise ex
    return _cache_id[path]
def get_api_path(id):
    if not dict_utils.has_key(_cache_id_revert,id):
        if _coll == None:
            from django.conf import settings
            load_from_django_settings()
            if _coll == None:
                raise (Exception("It look like you forgot call api.connect on settings.py\n"
                                 "\t\tHow to use this?:\n"
                                 "\t\t\tIn settings.py:\n"
                                 "\t\t\t\t\t  from quicky import api\n"
                                 "\t\t\t\t\t  api.connect(\n"
                                 "\t\t\t\t\t  host=db host,\n"
                                 "\t\t\t\t\t  port=db port,\n"
                                 "\t\t\t\t\t  name=db name,\n"
                                 "\t\t\t\t\t  user=db user name,\n"
                                 "\t\t\t\t\t  password=db password,\n"
                                 "\t\t\t\t\t  collection=the name of collection storage api)\n"
                                 ))
        lock.acquire()
        try:
            item = _coll.find_one({
                "api_id": {
                    "$regex": re.compile("^" + id + "$", re.IGNORECASE)
                }
            })
            if item==None:
                raise (Exception("'"+id+"' was not found"))
            _cache_id.update({
                item["api_path"]: item["api_id"]
            })
            _cache_id_revert.update({
                id: item["api_path"]
            })
            lock.release()
            return _cache_id_revert[id]



        except Exception as ex:
            lock.release()
            logger.debug(ex)
            raise ex

    return _cache_id_revert[id]
def logout(request):
    from django.shortcuts import redirect
    from django.contrib.auth import logout as signout
    from . import tenancy
    signout(request, request.user.schema)


