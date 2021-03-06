from . import *
from . import expr
from . import validators
from . filter_expression import filter_expression
from . aggregate_expression import aggregate_expression
from . import  aggregate_validators as query_validator
from . import validators
from .. import dict_utils
from .. fx_model import __obj_model__
from datetime import datetime
class _obj(object):
    pass



global models
models=_obj()
__py_types_map__={
    str:"string",
    float:"numeric",
    datetime:"date",
    bool:"bool",
    list:"array",
    object:"object",
    int:"int",
    "text":"text",
    "string":"text",
    "numeric":"numeric",
    "date":"date",
    "bool":"bool",
    "list":"list",
    "object":"object",
    "int":"int"
}
__mongodb_types_map__={
    str: "text",
    float: "numeric",
    datetime: "date",
    bool: "bool",
    list: "list",
    object: "object",
    int: "int",
    "text":"text",
    "string":"text",
    "numeric":"numeric",
    "date":"date",
    "bool":"bool",
    "list":"list",
    "object":"object",
    "int":"int"

}
from . model_events import model_event
_model_caching_={}
_model_index_={}
_model_caching_params={}
_model_events={}
_origin_fields ={}
class data_field():
    """
    Create data field for modle
    """
    data_type="text"
    is_require = False
    details=None
    def __init__(self,data_type="text",is_require=False,detail=None):
        # type: (str, bool, dict) -> object
        """
        Create data field for model
        :param data_type:field type default value is 'text'. The orther value must be 'bool','number','list' or 'object'
        :param is_require:
        :param detail:
        """
        self.is_require=is_require
        if __mongodb_types_map__.has_key(data_type):
            self.data_type=__mongodb_types_map__[data_type]
        else:
            raise (Exception("'{0}' is not support ".format(data_type.__str__())))
        self.details=detail
def convert_tuple_declare_into_fields(data):
    if data == None:
        return None
    if type(data) in [str,unicode]:
        return data
    _data = {}

    for k,v in data.items():
        if type(v) in [str,unicode]:
            _data.update({
                k: data_field(v)
            })
        elif v is dict:
            c=v
        elif not (type(v) is dict) and not (type(v) is tuple) and __py_types_map__.has_key(v):
            try:
                _data.update({
                    k: data_field(__py_types_map__[v])
                })
            except Exception as ex:
                x=ex


        elif type(v) is tuple:
            data_type = v[0]
            is_require = False
            detail= None
            if v.__len__()>1:
                is_require = v[1] != False
            if v.__len__() >2:
                detail= convert_tuple_declare_into_fields(v[2])
                _data.update({
                    k:data_field(data_type,is_require,detail)
                    })
            else:
                _data.update({
                    k: data_field(data_type, is_require, None)
                })


        else:
            _data.update({
                k: v
            })

    return _data
def create_obj_fields(data):
    if data == None:
        return None
    ret = _obj()
    for k,v in data.items():
        if v["type"] == "list":
            setattr(ret,v,[])
        elif v["type"] == "object":
            setattr(ret, v, create_obj_fields(v))
    return ret
def vert_expr(str,*params):
    """
    Parameterize expression
    :param str:
    :param params:
    :return:
    """
    ret=str
    index=0
    for p in params:
        ret=ret.replace("{"+index.__str__()+"}","get_params("+index.__str__()+")")
        index=index+1
    return ret
def filter(expression,*args,**kwargs):
    # type: (str, tuple|str|bool|int, dict) -> filter()|filter_expression
    """
    Create a filter for mongodb from expression
    :param expression: Filter expression
    :param args: primitive value or dict or tuple
    :param kwargs:
    :return:filter_expression will call by get_filter
    """
    params= args
    expr = expression
    _expr = expression
    if type(params) is tuple and params.__len__() > 0 and type(params[0]) is dict:
        _params = []
        _expr = expr
        _index = 0
        for key in params[0].keys():
            _expr = _expr.replace("@" + key, "{" + _index.__str__() + "}")
            _params.append(params[0][key])
            _index += 1
        expr = _expr
        params = _params
    elif params == ():
        _params = []
        _expr = expr
        _index = 0;
        for key in kwargs.keys():
            _expr = _expr.replace("@" + key, "{" + _index.__str__() + "}")
            _params.append(kwargs[key])
            _index += 1
        expr = _expr
        params = _params
    if expression.count("@")>0:
        _expr = vert_expr(_expr, *params)
        ret = filter_expression(_expr, *params)
        return ret
    else:
        _expr = vert_expr(_expr, *params,**kwargs)
        ret = filter_expression(_expr, *params,**kwargs)
        return ret

# def aggregate():
#     ret=aggregate_expression()
#     return ret
# def find(*args,**kwargs):
#     pass
def unwind_data(data,prefix=None):
    # type: (dict,str)->dict
    """
    convert dict with nested field into none nested filed
    :param data:dict to convert
    :param prefix:
    :return:dict
    """
    ret={}
    for key in data.keys():
        if type(data[key]) is dict:
            if prefix!=None:
                _prefix=prefix+"."+key
            else:
                _prefix = key
            ret_keys=unwind_data(data[key],_prefix)
            ret.update(ret_keys)
        elif isinstance(data[key],data_field):
            if data[key].data_type in ["list","object"]:
                if prefix!=None:
                    ret.update({
                        prefix + "." + key: {
                            "require": data[key].is_require,
                            "type":data[key].data_type,
                            "details":data[key].details
                        }
                    })
                else:
                    ret.update({
                        key: {
                            "require": data[key].is_require,
                            "type":data[key].data_type,
                            "details":data[key].details
                        }
                    })
                if data[key].details != None and not type(data[key].details) is str:
                    ret_fields = unwind_data(data[key].details, key)
                    if data[key].is_require:
                        ret.update({
                            key:{
                                "require":True,
                                "type":data[key].data_type
                            }
                        })
                    for k,v in ret_fields.items():
                        if k.__len__()>key.__len__() and k[0:key.__len__()+1] == key+".":
                            if prefix!=None:
                                ret.update({
                                    prefix + "."+k:  v
                                })
                            else:
                                ret.update({
                                    k: v
                                })
            else:
                if prefix!=None:
                    ret.update(
                        {
                            prefix + "." + key:{
                                "require":data[key].is_require,
                                "type":data[key].data_type
                            }
                        }
                    )
                else:
                    ret.update(
                        {
                            key: {
                                "require": data[key].is_require,
                                "type": data[key].data_type
                            }
                        }
                    )
    return ret
def define_model(_name,keys=None,*args,**kwargs):
    # type: (str,list,tuple)->query_validator.validator
    """
    Create model
    :param _name: model name
    :param keys: list of unique key of model exp:[['a','b'],['c','d']]
    :param args: dict descride model example: dict(code=helpers.create_field("code",True),..)
    :param kwargs:
    :return:
    """
    global _model_index_
    global _model_caching_params
    name=_name

    if dict_utils.has_key(_model_caching_,name):
        return _model_caching_[name]
    _obj_model = __obj_model__(name)
    setattr(models, name, _obj_model)
    _params=kwargs

    if type(args) is tuple and args.__len__()>0:
        _params=args[0]
    params = convert_tuple_declare_into_fields(_params)
    _model_caching_params.update({
        name:params
    })

    list_of_fields=unwind_data(params)
    _origin_fields.update({
        name:params
    })
    validators.set_require_fields(name,[
        x for x in list(list_of_fields.keys()) if list_of_fields[x]["require"]
    ])
    validate_dict={}
    for x in list_of_fields.keys():
        validate_dict.update(
            {
                x:list_of_fields[x]["type"]
            }
        )
    validators.create_model(name,validate_dict)
    _model_caching_.update({
        name:query_validator.validator(name,validate_dict),

    })
    _model_index_.update({
        name:{
                "keys":keys,
                "has_created":False
            }
        })

    for k,v in _model_caching_[name].meta.items():
        _obj_model.__create_field__(k,v)
    return _model_caching_[name]
def extent_model(name,from_name,keys=None,*args,**kwargs):
    # type: (str,str,list,dict)->query_validator.validator
    """
    Create a new model by extent an existing model
    :param name:new model name
    :param from_name:the name of existing model that this model will be extend
    :param keys:the unique key, this model will inherit unique key of base model
    :param args:dict describe of extent fields
    :param kwargs:
    :return:
    """
    # global models
    source_model=get_model(from_name)
    source_model_params=_model_caching_params[from_name]
    if type(args) is tuple and args.__len__()>0:
        for key in source_model_params.keys():
            args[0].update({
                key:source_model_params[key]
            })
    if keys==None:
        keys=[]
    keys.extend(_model_index_[from_name]["keys"])
    if dict_utils.has_key(_model_caching_params,from_name):
        kwargs.update(_model_caching_params[from_name])
    define_model(name,keys,*args,**kwargs)
    from_event=events(from_name)

    if from_event!=None:
        model_event = events(name)
        for f in from_event._on_before_insert:
            model_event.on_before_insert(f)
        for f in from_event._on_after_insert:
            model_event.on_after_insert(f)
        for f in from_event._on_before_update:
            model_event.on_before_update(f)
        for f in from_event._on_after_update:
            model_event.on_after_update(f)




    model=define_model(name,keys,*args,**kwargs)

def get_keys_of_model(name):
    """
    get list of key field of model
    :param name:
    :return:
    """
    return _model_index_[name]
def get_model(name):
    # type: (str)->query_validator.validator
    """
    get model by model name
    :param name:
    :return:
    """
    if not dict_utils.has_key(_model_caching_,name):
        raise (Exception("It look like you forgot create model for '{0}'\n"
                         "How to define a model?\n"
                         "from quicky import helpers\n"
                         "helpers.define_model(\n"
                         "\tYour model name here,\n"
                         "\tlist of key fields here,\n"
                         "\tfield name =helpers.create_field(""text|bool|numeric|date|list"",require or not)\n"
                         "\tor field name =dict(neasted field),..,\n"
                         "\tfield name n =helpers.create_field(""text|bool|numeric|date|list"",require or not))".format(name)))
    return _model_caching_[name]
def create_field(data_type="text",is_require=False,detail=None):
    # type: (str, bool, dict) -> data_field
    """
    :param=data_type: type of model field default value is 'text'. The orther value must be 'bool','number','list' or 'object'
    :param=is_require: is model field require? default value is 'False'
    :param=detail: detail definition of this feild if it is a list type model field
    :return= data_field object
    """
    return data_field(data_type,is_require,detail)
def extract_data(data):
    # type: (dict) -> dict
    """
    convert data dict into a dict including key and value with primitive value, example: {a:{b:1,c:{d:1}}}=>{{'a.b':1},{'a.b.c.d';1}}
    :param data:
    :return:
    """
    ret={}
    for key in data.keys():
        if key.find(".")>-1:
            items=key.split('.')
            if not dict_utils.has_key(ret,items[0]):
                ret.update({
                    items[0]:{}
                })
            val=ret[items[0]]
            for x in items[1:items.__len__()-1]:
                if not dict_utils.has_key(val,x):
                    val.update({
                        x:{}
                    })
                val=val[x]
            val.update({
                items[items.__len__() - 1]:data[key]
            })

        else:
            ret.update({
                key:data[key]
            })
    return ret
def events(name):
    # type: (str) -> list
    """
    Get list of events of model by model name
    :param name: Model name
    :return: list of function has been declare in model
    """
    if dict_utils.has_key(_model_events,name):
        return _model_events[name]
    else:
        _model_events.update({
            name:model_event()
        })
        return _model_events[name]
def extends_dict(data,*args,**kwargs):
    ret= data.copy()
    x=kwargs
    if type(args) is tuple and args.__len__()>0:
       x =  args[0]
    ret.update(x)
    return ret
def merge_dict(a,b):
    if type(a) is dict:
        r=a.copy()
    else:
        r ={}
    for k,v in b.items():
        if r.has_key(k):
            if type(v) is dict:
                m = merge_dict(r[k],v)
                r.update({k:m})
            else:
                r.update({k: v})
        else:
            r.update({k:v})
    return r
def __replace_dot_number_of_dict__(a):
    import re
    ret = {}
    for k,v in a.items():
        keys=re.findall(r"\.\d+\.",k)
        tmp_k =k
        for x in keys:
            tmp_k=tmp_k.replace(x,"_$dot$_"+x[1:x.__len__()-1]+"_$dot$_")
        ret.update({tmp_k:v})
    return ret
def __replace_dolar_dot_dolar_dot__(a):
    ret ={}
    for k,v in a.items():
        if type(v) is dict:
            ret.update({
                k.replace("_$dot$_","."):__replace_dolar_dot_dolar_dot__(v)
            })
        else:
            ret.update({
                k.replace("_$dot$_", "."): v
            })
    return ret
def slice_key_of_dict(d):
    a= __replace_dot_number_of_dict__(d)
    ret_val = {}
    for k,v in a.items():
        ret ={}
        if k.count('.')>0:
            items= k.split('.')
            tmp=iter = {}
            for i in range(0,items.__len__()-1):
                iter.update({
                    items[i]:{}
                })
                iter=iter[items[i]]
            iter.update({
                items[items.__len__()-1]:v
            })
            ret.update(tmp)
        else:
            ret.update({k:v})
        ret_val = merge_dict(ret_val,ret)
    ret_dict = __replace_dolar_dot_dolar_dot__(ret_val)
    return ret_dict

