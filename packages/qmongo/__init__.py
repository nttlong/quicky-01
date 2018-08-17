class _obj(object):
    pass
def create_object(*args,**kwargs):
    ret = _obj()
    data = {}
    if type(args) is tuple and args.__len__()>0:
        data = args[0]
    else:
        data = kwargs
    for k,v in data.items():
        if type(v) is dict:
            setattr(ret,k,create_object(v))
        else:
            setattr(ret, k, v)
    return ret
from . import models
from . import helpers
