import pydoc

__models__ = None

import pydoc

fields = pydoc.fields ()




class BaseModelDefinition (object):
    def __init__(self, name):
        # type: (object) -> object
        """
        :type name: str

        """
        self.name = name
        global __models__
        if __models__ == None:
            __models__ = {}
        __models__.update ({
            name: {}
        })


class ModelDefinition (BaseModelDefinition):
    def set_indexes(self, indexes):
        self.indexes = indexes
        self.fields = {}
        self.name = "";
        self.required = None
        return self
class PartialFilterExpression (object):
    def __init__(self, expr, *args, **kwargs):
        self.__data__ = pydoc.compile (expr, *args, **kwargs)
class IndexOption (object):
    def __init__(self,
                 background=True,
                 unique=False,
                 name=None,
                 partialFilterExpression=None,
                 sparse=None,
                 expireAfterSeconds=None):

        self.background = background
        if unique != None:
            self.unique = unique
        if name != None:
            self.name = name
        if partialFilterExpression != None:
            if isinstance (partialFilterExpression, PartialFilterExpression):
                self.partialFilterExpression = partialFilterExpression.__data__
        if sparse != None:
            self.sparse = True

        self.expireAfterSeconds = 10
class Index (object):
    def __init__(self, fields, options=None):
        # type: (str|dict|pydoc.Fields|tuple(pydoc.Fields)|tuple(str)|list(pydoc.Fields)|list(str), IndexOption) -> object
        import pydoc
        self.fields = {}
        if isinstance (fields, tuple) or isinstance (fields, list):
            for item in fields:
                if type (item) in [str, unicode]:
                    self.fields.update ({
                        item: 1
                    })
                elif isinstance (pydoc.Fields):
                    self.fields.update ({
                        pydoc.get_field_expr (item, True): 1
                    })
        if isinstance (fields, pydoc.Fields):
            self.fields.update ({
                pydoc.get_field_expr (fields, True): 1
            })
        elif type (fields) in [str, unicode]:
            self.fields.update ({
                fields: 1
            })

        if isinstance (options, IndexOption):
            self.options = options
class FieldInfo (object):
    def __init__(self, fieldType, required=None, detail=None):
        self.fieldType = None
        self.required = required
        self.detail = detail


        if not isinstance (fieldType, type):
            raise Exception ("'fieldType' must be type, not value")
        self.fieldType = fieldType
        if detail != None:
            if not isinstance (detail, dict):
                raise Exception ("'detail' must be dict")
            ret = __extract_fields__ (detail)
            self.detail = ret
def __extract_fields__(fields):
    ret = {}
    for k, v in fields.items ():
        _k = k
        if isinstance (k, pydoc.Fields):
            _k = pydoc.get_field_expr (k, True)
        if isinstance (v, type):
            ret.update ({
                _k: FieldInfo (v)
            })
        elif isinstance (v, dict):
            ret.update ({
                k: FieldInfo (object, None, __extract_fields__ (v))
            })
        elif isinstance (v, FieldInfo):
            ret.update ({
                _k: v
            })

    return ret
def create_model(name, required, indexes, fields):
    # type: (str, list, object) -> object
    if type (name) not in [str, unicode]:
        raise Exception ("'{0}' must be str or unicode".format ("name"))
    instance_model = ModelDefinition (name)
    global __models__

    if isinstance (indexes, list):
        instance_model.set_indexes (indexes)
    if required != None:
        if not isinstance (required, list):
            raise Exception ("'{0}' must be None or list".format ("required"))
        else:
            instance_model.required = []
            for item in required:
                if isinstance (item, pydoc.Fields):
                    instance_model.required.append (pydoc.get_field_expr (item, True))
                else:
                    instance_model.indexes.append (item)
    instance_model.fields = __extract_fields__ (fields)
    if __models__ == None:
        __models__ = {}
        __models__.update ({
            name: instance_model
        })
    doc = Document(name,None)
    __create_doc__(doc,instance_model.fields)
    setattr(documents,name,doc)

    return instance_model
def get_model(name):
    global __models__
    if __models__ == None:
        return None
    return __models__.get (name, None)

import mobject
documents = mobject.dynamic_object({})
__doc_dict__ = {}
def __create_instance_from_type__(data,data_type):
    ret =DocumentInstance(data.__name__)
    for k,v in data.__dict__.items():
        if not (k.__len__()>2 and k[0:2]=="__" and k[k.__len__()-2:k.__len__()]=="__"):
            if isinstance(v,Document):
                master_data_type,data_type = getattr(data,k).__dict__["__dict__"]["__data_type__"]
                if master_data_type == list:
                    setattr (ret, k,([], __create_instance_from_type__ (v, data_type)))
                else:
                    setattr(ret,k,(master_data_type,__create_instance_from_type__(v,data_type)))
            elif isinstance(v,tuple):
                setattr (ret, k, v[0])
            else:
                setattr(ret,k,v)
    ret.__dict__.update({
        "__is_init_complete__":True
    })
    return ret

class BaseDocumentInstance(object):
    def __init__(self,name,*args,**kwargs):
        self.__dict__ = {
            "__type__":{},
            "__is_in_init__":True,
            "__name__":name
        }

        self.__is_in_init__ = True
class DocumentInstance(BaseDocumentInstance):
    def __setattr__(self, key, value):
        ancestor = super(DocumentInstance,self)
        if key =="__dict__":
            ancestor.__dict__.update(value)
            return
        if key in [ "__type__", "__is_in_init__"]:
            ancestor.__dict__.update({
                key:value
            })
        is_init_complete = ancestor.__dict__.get ("__is_init_complete__", False)
        if isinstance(value,tuple):
            if value[0]==[]:
                if ancestor.__dict__.get ("__type__", None) == None:
                    ancestor.__dict__.update ({
                        "__type__": {}
                    })
                ancestor.__dict__["__type__"].update ({
                    key: list
                })
                ancestor.__dict__.update ({
                    key: []
                })
                return

        if isinstance(value,DocumentInstance):
            if not is_init_complete:
                if ancestor.__dict__.get("__type__",None) == None:
                    ancestor.__dict__.update({
                        "__type__":{}
                    })
                ancestor.__dict__["__type__"].update ({
                    key: dict
                })
            ancestor.__dict__.update({
                key:value
            })

        else:

            if not is_init_complete:
                if ancestor.__dict__.get("__type__",None) == None:
                    ancestor.__dict__.update({
                        "__type__":{}
                    })
                ancestor.__dict__.update ({
                    key: None
                })
                if value == list:
                    x= value
                ancestor.__dict__["__type__"].update({
                    key:value
                })

            else:
                if not ancestor.__dict__["__type__"].has_key(key):
                    raise Exception("'{0}' was not found".format(key))
                data_type = ancestor.__dict__["__type__"][key]
                if type(value) is data_type:
                    if data_type == dict:
                        if isinstance(value,DocumentInstance):
                            ancestor.__dict__.update ({
                                key: __create_instance_from_type__ (value)
                            })
                        else:
                            raise Exception("{0} must be DocumentInstance of {0}".format(ancestor.__dict__["__name__"]+"."+key))
                    elif type == list:
                        ret_list =[]
                        for item in value:
                            ret_list.append(__create_instance_from_type__)
                    else:
                        ancestor.__dict__.update ({
                            key: value
                        })
                else:
                    raise Exception("{0} is not {1}".format(value,data_type))






class BaseDocument(object):
    def __init__(self,name,data_type):
        self.__dict__ = {
            "__type__": {},
            "__doc__": pydoc.Fields (),
            "__data_type__":data_type
        }
        self.__name__ = name
class Document(BaseDocument):
    def __setattr__(self, key, value):
        ancestor = super(Document,self)
        ancestor.__dict__.update({key:value})
    def __getattr__(self, item):
        owner = super (Document, self)
        if item == "__dict__":
            return owner.__getattribute__ (item)
        else:
            return owner.__dict__.get (item)
    def field(self):
        return pydoc.Fields()
    def object(self):
        return __create_instance_from_type__(self,None)




def __create_doc__(doc,fields):
    for k,v in fields.items():
        sub_type = object
        if isinstance(v.detail,type):
            sub_type=v.detail
        setattr (doc, k, (v.fieldType,sub_type))
        if v.detail != None:
            sub_doc = Document(doc.__name__+"."+k,(v.fieldType,sub_type))
            _p = getattr(doc,k)
            __create_doc__(sub_doc,v.detail)
            setattr(doc,k,sub_doc)




