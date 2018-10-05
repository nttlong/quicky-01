# encoding=utf8
VERSION = [1,0,0,"beta",0]
def get_version():
    return VERSION[0].__str__()+\
           "."+VERSION[1].__str__()+\
           "."+VERSION[2].__str__()+\
           "."+VERSION[3].__str__()+\
           "."+VERSION[4].__str__()
__config=None
def set_config(*args,**kwargs):
    params=kwargs
    if args.__len__()>0:
        params=kwargs
    global __config
    __config=params
def get_config():
    global __config
    return __config
def get_url_server():
    global __config
    return __config["url"]
def get_auth():
    return (__config["user"],__config["password"])

from . import reports