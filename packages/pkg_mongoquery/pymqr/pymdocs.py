
class BaseModel (object):
    def __init__(self):
        import pydoc
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
        import pydoc
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
class BaseEmbededDoc (object):
    pass
def ___consume_attr_field__(param, key, value):
    if isinstance (value, BaseEmbededDoc):
        for k, v in value.__dict__.items ():
            param.update ({
                key + "." + k: v
            })
            ___consume_attr_field__ (param, key + "." + k, v)