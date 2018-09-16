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
def template(fn,*args,**kwargs):
    path = None
    if type(args) is tuple and args.__len__() == 0:
        path = kwargs.get("file","unknown.html")
        is_public = kwargs.get("is_public",False)
    else:
        path =args[0]
    instance = executor.executor(fn,path)
    return instance.execute_request(True)








