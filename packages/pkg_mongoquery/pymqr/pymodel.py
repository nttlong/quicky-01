import pydoc

__models__ = None

import pydoc

fields = pydoc.fields ()


class BaseEmbededDoc (object):
    pass


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


def ___consume_attr_field__(param, key, value):
    if isinstance (value, BaseEmbededDoc):
        for k, v in value.__dict__.items ():
            param.update ({
                key + "." + k: v
            })
            ___consume_attr_field__ (param, key + "." + k, v)


class BaseModel (object):
    def __init__(self):
        self.__dict__ = {
            "__fields_types__": {},
            "__fields_docs__": pydoc.Fields (),
            "__model_name__": None
        }

    def __getattr__(self, field):
        # if not self.__dict__["__fields_types__"].has_key(field):
        #     raise Exception("{0} was not found ".format(field))
        items = field.split ('.')
        ret = self.__dict__["__fields_docs__"]
        for item in items:
            ret = getattr (ret, item)
        return ret

    def __setattr__(self, key, value):
        if not self.__dict__.has_key ("__fields_types__"):
            self.__dict__.update ({
                "__fields_types__": {}
            })

        if not self.__dict__.has_key ("__fields_docs__"):
            self.__dict__.update ({
                "__fields_docs__": pydoc.fields ()
            })

        self.__dict__["__fields_types__"].update ({
            key: value
        })
        if isinstance (value, BaseEmbededDoc):
            for k, v in value.__dict__.items ():
                self.__dict__["__fields_types__"].update ({
                    key + "." + k: v
                })
                ___consume_attr_field__ (self.__dict__["__fields_types__"], key + "." + k, v)

    def set_model_name(self, name):
        self.__dict__.update ({
            "__model_name__": name
        })

    def get_model_name(self):
        return self.__dict__.get ("__model_name__", None)


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
    return instance_model


def get_model(name):
    global __models__
    if __models__ == None:
        return None
    return __models__.get (name, None)




