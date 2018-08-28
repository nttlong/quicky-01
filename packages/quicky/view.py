from . import extens
from . import applications
from . import language

from . import authorize
import threading
import logging
import os
import sys
from . import tenancy
logger=logging.getLogger(__name__)
global lock
settings=None
lock=threading.Lock()
_cache_view={}
import executor
def template_uri(fn):

    def layer(*args, **kwargs):
        def repl(f):
            return fn(f, *args, **kwargs)
        return repl
    return layer
@template_uri
def template(fn,*_path,**kwargs):

    # if _path.__len__()==1:
    #     _path=_path[00]
    # if _path.__len__()==0:
    #     _path=kwargs
    # app = None
    # if sys.version_info[0] <= 2:
    #     app=applications.get_app_by_file(fn.func_code.co_filename)
    # else:
    #     app = applications.get_app_by_file(fn.__code__.co_filename)
    #
    # setattr(fn,"__application__",app)
    instance = executor.executor(fn,_path)
    return instance.execute_request(True)

    # if is_multi_tenancy:
    #     if app == None:
    #         return exec_request
    #     elif hasattr(app.settings, "DEFAULT_DB_SCHEMA"):
    #         if app.host_dir == "":
    #             return exec_request
    #         else:
    #             return exec_request
    #     else:
    #         return exec_request_for_mul
    #
    # else:
    #     return exec_request







