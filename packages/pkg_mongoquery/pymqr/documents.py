__fields_types__ = "__fields_types__"  # key of field type
__fields_docs__ = "__fields_docs__"  # key of field value
__fields_default_value__ = "__fields_default_value__"  # key of default value field
__model_name__ = "__model_name__"  # type: str # key of model name
__map_doc__ =None
class ___CollectionMapClassWrapper__():
    def __init__(self,name):
        self.name = name
    def wrapper(self,*args,**kwargs):
        global __map_doc__
        if __map_doc__==None:
            __map_doc__={}
        __map_doc__.update({
            args[0]:self.name
        })
def Collection(*args,**kwargs):
    ret = ___CollectionMapClassWrapper__()
    return ret.wrapper

class exceptions():
    class InvalidDataType(Exception):
        def __init__(self, field_name, expectect_data_type, receive_data_type):
            self.message = "The data type of {0} is {1}, not {2}".format(field_name, expectect_data_type,
                                                                         receive_data_type)
            self.field_name = field_name
            self.expectect_data_type = expectect_data_type
            self.receive_data_type = receive_data_type
            super(Exception, self).__init__(self.message)

    class MissingData(Exception):
        def __init__(self, field_name):
            self.message = "{0} is require".format(field_name)
            self.field_name = field_name
            super(Exception, self).__init__(self.message)


class __GOBBLE__():
    @staticmethod
    def get_dict_fields(data):
        if isinstance(data, dict):
            if not data.has_key(__fields_docs__):
                data.update({__fields_docs__: {}})
            return data[__fields_docs__]
        else:
            raise Exception("invalid param")

    @staticmethod
    def get_dict_fields_type(data):
        if isinstance(data, dict):
            if not data.has_key(__fields_types__):
                data.update({__fields_types__: {}})
            return data[__fields_types__]
        else:
            raise Exception("invalid param")

    @staticmethod
    def get_dict_default_value(data):
        if isinstance(data, dict):
            if not data.has_key(__fields_default_value__):
                data.update({__fields_default_value__: {}})
            return data[__fields_default_value__]
        else:
            raise Exception("invalid param")

    @staticmethod
    def set_attr_field(param, key, value):
        if isinstance(value, BaseEmbededDoc):
            for k, v in value.__dict__.items():
                param.update({
                    key + "." + k: v
                })
                __GOBBLE__.gobble_attr_field(param, key + "." + k, v)

    @staticmethod
    def dictionary(value):
        if isinstance(value, dict):
            import pydocs
            ret_val = {}
            for k, v in value.items():
                _k = k
                if isinstance(k, pydocs.Fields):
                    _k = pydocs.get_field_expr(k, True)
                ret_val.update({_k: __GOBBLE__.dictionary(v)})
            return ret_val
        else:
            return value


class BaseDocumentsInstance(object):
    def __setattr__(self, key, value):
        if not self.__dict__["__type__"].has_key(key):
            raise exceptions.MissingData(key)
        if value != None and type(value) != self.__dict__["__type__"][key]:
            raise exceptions.InvalidDataType(key, self.__dict__["__type__"][key], type(value))
        self.__dict__.update({
            key: value
        })

    def doc(self):
        import pydocs
        return pydocs.Fields()

    def filter(self):
        import pydocs
        return pydocs.Fields(None, True)

    # def __setitem__(self, key, value):
    #     x=item


class BaseDocuments(object):
    def __init__(self):
        import pydocs
        global __map_doc__
        if __map_doc__ == None:
            __map_doc__ ={}
        self.__dict__ = {
            __fields_types__: {},
            __fields_docs__: pydocs.Fields(),
            __model_name__:__map_doc__.get(type(self))
        }

    def __getattr__(self, field):
        import pydocs
        # if not self.__dict__["__fields_types__"].has_key(field):
        #     raise Exception("{0} was not found ".format(field))
        items = field.split('.')
        ret = __GOBBLE__.get_dict_fields(self.__dict__)
        if ret.has_key(field):
            return ret[field]
        else:
            ret.update({
                field: pydocs.Fields(field)
            })
            return ret[field]

    def __setattr__(self, key, value):
        import pydocs
        _value = value
        _default = None
        if isinstance(value, tuple):
            _value, _default = value
        _fields_type_ = __GOBBLE__.get_dict_fields_type(self.__dict__)
        _fields_default_ = __GOBBLE__.get_dict_default_value(self.__dict__)
        _fields_ = __GOBBLE__.get_dict_fields(self.__dict__)
        _fields_type_.update({key: _value})
        _fields_default_.update({key: _default})

    def set_model_name(self, name):
        self.__dict__.update({
            "__model_name__": name
        })

    def get_model_name(self):
        return self.__dict__.get("__model_name__", None)

    def load(self,*args,**kwargs):
        if args.__len__()>0:
            return self.object(args[0])
        else:
            return self.object(kwargs)
    def object(self, data=None):
        import pydocs
        from inspect import isfunction
        if data == None:
            value = {}
        else:
            value = data
        value = __GOBBLE__.dictionary(value)

        field_types = __GOBBLE__.get_dict_fields_type(self.__dict__)
        field_defaults = __GOBBLE__.get_dict_default_value(self.__dict__)

        ret_data = {
            "__type__": field_types
        }
        for k, v in field_types.items():
            if issubclass(field_types[k], BaseEmbededDoc):
                data_value = value.get(k, None)

                try:
                    x = field_types[k]()  # create new instance
                    if data_value == None:
                        default_values = __GOBBLE__.get_dict_default_value(self.__dict__)
                        if default_values.has_key(k):
                            default_value = __GOBBLE__.dictionary(default_values[k])
                            if isfunction(default_value):
                                child = x.object(default_values[k]())
                            else:
                                child = x.object(default_value)
                            ret_data.update({
                                k: child
                            })
                        else:
                            child = x.object()
                            ret_data.update({
                                k: child
                            })
                    else:
                        child = x.object(data_value)
                        ret_data.update({
                            k: child
                        })
                except exceptions.MissingData as ex:
                    raise exceptions.MissingData(k + "." + ex.field_name)

                    # if self.__dict__.has_key("__name__"):
                    #     x.__dict__.update({"__name__": self.__dict__["__name__"]+"."+ k})
                    # else:
                    #     x.__dict__.update({"__name__": k})
                    # child = x.object(value.get(k,None))
                    # ret_data.update ({
                    #     k: child
                    # })
            else:
                _v = value.get(k, None)
                _d = field_defaults[k]
                if _v != None and isinstance(_v, dict):
                    raise Exception("type of {0} is {1}".format(k, type(v)))
                if _v == None:
                    if v == list:
                        ret_data.update({
                            k: []
                        })

                    elif _d == None and not hasattr(self, "__name__") and issubclass(v, BaseDocuments):
                        raise Exception("'{0}' can not be empty".format(k))
                    else:
                        if isfunction(_d):
                            ret_data.update({
                                k: _d()
                            })
                        else:
                            if not issubclass(v, BaseDocuments) and _d == None:
                                field_name = k

                                if self.__dict__.has_key("__name__"):
                                    field_name = self.__dict__["__name__"] + "." + field_name
                                raise exceptions.MissingData(field_name)
                            ret_data.update({
                                k: _d
                            })
                else:
                    import types
                    if isfunction(_v) or isinstance(_v, types.BuiltinFunctionType):
                        _v = _v()
                    if type(_v) != field_types[k]:
                        field_name = k
                        if self.__dict__.has_key("__name__"):
                            field_name = self.__dict__["__name__"] + "." + k
                        raise exceptions.InvalidDataType(field_name, field_types[k], type(_v))
                    ret_data.update({
                        k: _v
                    })

        ret = BaseDocumentsInstance()
        ret.__dict__.update(ret_data)
        ret.__dict__.update({
            "__docs__": self
        })
        return ret

    def __lshift__(self, other):
        if other == {}:
            raise Exception("Can not fill data into {0} with empty dict".format(type(self)))
        return self.object(other)

    def __is_contains_field__(self, item):
        import pydocs
        _field_ = item
        if isinstance(item, pydocs.Fields):
            _field_ = pydocs.get_field_expr(item, True)
        items = _field_.split('.')
        if items.__len__() == 1:
            return __GOBBLE__.get_dict_fields_type(self.__dict__).has_key(items[0])
        else:
            next_field = ".".join([x for x in items if items.index(x) > 0])
            child_object = __GOBBLE__.get_dict_fields_type(self.__dict__)[items[0]]()
            return child_object.__is_contains_field__(next_field)

    def __contains__(self, item):
        _is_check_one_of_ = False
        _fields = item
        if isinstance(item, set):
            _fields = list(item)
            _is_check_one_of_ = True
        if isinstance(item, tuple):
            _fields = list(item)
        if not isinstance(_fields, list):
            _fields = [_fields]
        if _is_check_one_of_:
            ok = False
            index = 0
            while index < _fields.__len__():
                if self.__is_contains_field__(_fields[index]):
                    return True
                else:
                    index += 1
            return False
        else:
            ok = True
            index = 0
            while index < _fields.__len__():
                ok = ok and self.__is_contains_field__(_fields[index])
                if not ok:
                    return ok
                else:
                    index += 1
            return ok


class BaseEmbededDoc(BaseDocuments):
    pass
