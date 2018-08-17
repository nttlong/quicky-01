class __obj__(object):
    pass
def create(*args,**kwargs):
    ret = __obj__()
    data = {}
    if type(args) is tuple and args.__len__()>0:
        data = args[0]
    else:
        data = kwargs
    for k,v in data.items():
        if type(v) is dict:
            setattr(ret,k,create(v))
        elif type(v) is list:
            setattr(ret, k, [create(_v) for _v in v])
        else:
            setattr(ret, k, v)
    return ret
def convert_to_dict(obj):
    if obj == None:
        return None
    ret = {}
    for k, v in obj.__dict__.items():
        if type(v) is list:
            ret.update({
                k:[convert_to_dict(_v) for _v in v]
            })
        elif hasattr(v,"__dict__"):
            ret.update({
                k:convert_to_dict(v)
            })
        else:
            ret.update({
                k: v
            })
    return ret




