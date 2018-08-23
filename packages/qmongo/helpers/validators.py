import threading
import datetime
global lock
from .. import dict_utils
lock=threading.Lock()
global _model_cache_
_model_cache_={
    "require_fields":{},
    "type_fields":{}
}
def get_value_by_path(path,data,return_with_key= False):
    """
    get value of dict by path to property, example: get_value_by_path("a.b",{a:b:"hello"}} -> "hello"
    :param path:
    :param data:
    :return:
    """
    parents = {}
    if dict_utils.has_key(data,path):
        return data[path],{}
    items=path.split(".")
    if items.__len__()==1:
        return data.get(items[0],None),{}
    else:
        val=data
        p_key =""
        for i in range(0,items.__len__()):
            if not type(val) is dict:
                if not return_with_key:
                    return None, parents
                else:
                    return val, p_key[0:p_key.__len__() - 1]
            val = val.get(items[i],None)

            parents.update({
                p_key[0:p_key.__len__() - 1]:val
            })
            if val == None:
                if not return_with_key:
                    return None,parents
                else:
                    return val, p_key[0:p_key.__len__() - 1]
            else:
                parent = val
            p_key = p_key + items[i] + "."
        if not return_with_key:
            return val,parents
        else:
            return val, p_key[0:p_key.__len__() - 1]

def validate_require_data_from_field(name,data,field):
    _model_ = _model_cache_['require_fields'][name]
    _ignore_ = [k for k,v in _model_cache_["type_fields"][name].items() if v == "list" and k.__len__() > field.__len__() and k[0:field.__len__()+1] == field +"." ]
    fields =[]
    for I in _ignore_:
        for x in _model_:
            if x.__len__() > field.__len__() and x[0:field.__len__() + 1] == field + ".":
                if not (x.__len__() > I.__len__() and x[0:I.__len__() + 1] == I + "."):
                    fields.append(x)
    ret = []
    for key in fields:

        # if key.count(".") == 0:
        val = get_value_by_path(key, data)
        if val == None:
            # if helpers._model_caching_[name].meta[key] == "list":

            ret.append(key)
    return ret
def validate_require_data(name,data,partial=False):
    """
    This function will check where is missing data in "data" according to model in "name"
    :param name:model name
    :param data:data will be verified
    :param partial:False will check full from model, True will check only fields in data
    :return: list of missing fields
    """
    # from .. import helpers
    # inogre_objects =[k for k,v in helpers._origin_fields[name].items() if v.data_type in ["object","list"]   and not v.is_require]
    if not partial:
        ret=[]
        for key in _model_cache_["require_fields"].get(name,["_id"]):

            # if key.count(".") == 0:
            val,parents =get_value_by_path(key,data)
            if val == None and parents =={}:
                ret.append(key)
            else:
                none_items = [k for k,v in parents.items() if v==None ]
                if none_items.__len__() == 0 and val == None:
                    ret.append(key)
                elif none_items.__len__()>0:
                    ret.append(none_items[0])

        ret_items = []
        for x in ret:
            if ret_items.count(x) ==0 and x != "":
                ret_items.append(x)
        return ret_items
    else:
        if data=={}:
            return []
        path=""
        val=data
        ret=[]
        for key in data.keys():
            if key[0:1]!="$":
                find_fields = [x for x in _model_cache_["require_fields"].get(name, []) if x[0:key.__len__()] == key]
                if find_fields.__len__() > 0:
                    # val = get_value_by_path(find_fields[0], data)
                    val, parents = get_value_by_path(find_fields[0], data)
                    if val == None and parents == {}:
                        ret.append(find_fields[0])
                    else:
                        if parents != {}:
                            none_items = [k for k, v in parents.items() if v == None]
                            if none_items != None:
                                if none_items.__len__() == 0:
                                    ret.append(find_fields[0])
                                else:
                                    ret.append(none_items[0])

        return ret
def set_require_fields(name,*args,**kwargs):
    """
    set require field name for model
    :param name:model name
    :param args:
    :param kwargs:
    :return:
    """

    if dict_utils.has_key(_model_cache_["require_fields"],name):
        pass
    else:
        lock.acquire()
        try:
            params = kwargs
            if type(args) is tuple and args.__len__() > 0:
                params = args[0]
            _model_cache_["require_fields"].update({
                name:params
            })
            lock.release()

        except Exception as ex:
            lock.release()
            raise(ex)
def create_model(name,*args,**kwargs):
    """
    Create model
    :param name: model name
    :param args: dic describe model fields
    :param kwargs:
    :return:
    """
    params=kwargs
    if type(args) is tuple and args.__len__()>0:
        params=args[0]
    if not dict_utils.has_key(_model_cache_["type_fields"],name):
        lock.acquire()
        try:
            _model_cache_["type_fields"].update({
                name:params
            })
            lock.release()
        except Exception as ex:
            lock.release()
            raise ex
def get_data_fields(data):
    """
    get all fields of data it serve for this file
    :param data:
    :return:
    """
    ret={}
    field_with_typpe_list=[x for x in data.keys() if data[x]=="list"]

    ignore_list=[]
    for key in field_with_typpe_list:
        ignore_list.extend([x for x in data.keys() if x.__len__()>key.__len__() and   x[0:key.__len__()+1]==key+"."])

    for key in data.keys():
        if data[key]=="list" :
            ret.update({
                key:"list"
                })
        elif ignore_list.count(key)==0:
            ret.update({
                key:data[key]
                })
    return ret



def validate_type_of_data(name,data):
    """
    Check data type of each field in data is compatible
    :param name:
    :param data:
    :return:
    """
    ret = []
    data_fields=get_data_fields(_model_cache_["type_fields"].get(name, {}))
    for key in data_fields:
        type_of_value = _model_cache_["type_fields"][name][key]
        if type_of_value in ["list","object"]:
            #val = get_value_by_path(key, data)
            #for item in val:
            #    val = get_value_by_path(key, item)
            pass
        else:
            val,parents = get_value_by_path(key, data,True)
            if type(parents) in [str,unicode] and parents!=key:
                ret.append(parents)
            else:
                if val != None:

                    if type_of_value == "text" and type(val) not in [str, unicode]:
                        ret.append(key)
                    if type_of_value == "numeric" and type(val) not in [
                        int,
                        float,
                        long,
                        complex
                    ]:
                        ret.append(key)
                    if type_of_value == "bool" and type(val) != bool:
                        ret.append(key)
                    if type_of_value == "date" and type(val) != datetime.datetime:
                        ret.append(key)
                    if type_of_value == "list" and type(val) != list:
                        ret.append(key)

    return [ x for x in ret if x!='']
