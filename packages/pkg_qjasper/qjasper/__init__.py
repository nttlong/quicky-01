# encoding=utf8
VERSION = [1,0,0,"beta",3]
from . import search_filter
def get_version():
    return VERSION[0].__str__()+\
           "."+VERSION[1].__str__()+\
           "."+VERSION[2].__str__()+\
           "."+VERSION[3].__str__()+\
           "."+VERSION[4].__str__()
__config=None
def set_config(*args,**kwargs):
    if args.__len__()==0 and kwargs=={}:
        raise Exception("Parameteres is missing:\n"
                        "\tExmaple:\n"
                        "\t\tqjasper.set_config(\n"
                        "\t\t\turl=<url to jasper server>,\n"
                        "\t\t\tuser=<username>,\n"
                        "\t\t\tpassword=<password>"
                        "\t\t\t)")
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
    if __config == None or not __config.has_key("url"):
        raise (Exception("It look likes you forgot call set_config of qjasper\n"
                         "How to use qjasper:\n"
                         "\t\timport qjasper\n"
                         "\t\t"))
    return __config["url"]
def get_auth():
    return (__config["user"],__config["password"])
from . search_filter import resource_types,resource_sort_fields
def filter(name_or_description=None,
                 folderUri=None,
                 type=resource_types.none,
                 sortBy=resource_sort_fields.none,
                 limit=50,
                 offset=0):
    return search_filter.filter(name_or_description,
                                folderUri,
                                type,
                                sortBy,
                                limit,
                                offset)
from . import reports
from . import resources