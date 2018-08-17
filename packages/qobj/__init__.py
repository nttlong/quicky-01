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