import pydoc
__models__=None

import pydoc
fields=pydoc.fields()
class BaseEmbededDoc (object):
    pass
class BaseModelDefinition(object):
    def __init__(self, name):
        # type: (object) -> object
        """
        :type name: str

        """
        self.name=name
        global __models__
        if __models__==None:
            __models__={}
        __models__.update({
            name:{}
        })
class ModelDefinition(BaseModelDefinition):
    def set_indexes(self, indexes):
        self.indexes=indexes
        return self


def ___consume_attr_field__(param, key, value):
    if isinstance(value,BaseEmbededDoc):
        for k, v in value.__dict__.items ():
            param.update ({
                key + "." + k: v
            })
            ___consume_attr_field__ (param, key + "." + k, v)




class BaseModel(object):
    def __init__(self):
        self.__dict__={
            "__fields_types__":{},
            "__fields_docs__":pydoc.Fields()
        }

    def __getattr__(self, field):
        if not self.__dict__["__fields_types__"].has_key(field):
            raise Exception("{0} was not found ".format(field))
        items = field.split('.')
        ret = self.__dict__["__fields_docs__"]
        for item in items:
            ret=getattr(ret,item)
        return ret
    def __setattr__( self, key, value):
        if not self.__dict__.has_key("__fields_types__"):
            self.__dict__.update({
                "__fields_types__":{}
            })

        if not self.__dict__.has_key("__fields_docs__"):
            self.__dict__.update({
                "__fields_docs__":pydoc.fields()
            })

        self.__dict__["__fields_types__"].update({
            key:value
        })
        if isinstance(value,BaseEmbededDoc):
            for k,v in value.__dict__.items():
                self.__dict__["__fields_types__"].update({
                    key+"."+k:v
                })
                ___consume_attr_field__(self.__dict__["__fields_types__"],key+"."+k,v)


        
class PartialFilterExpression(object):
    def __init__(self,expr,*args,**kwargs):
        self.__data__= pydoc.compile(expr,*args,**kwargs)

class IndexOption(object):
    def __init__(self,
                 background=True,
                 unique=False,
                 name=None,
                 partialFilterExpression=None,
                 sparse=None,
                 expireAfterSeconds=None):

        self.background=background
        if unique!=None:
            self.unique=unique
        if name!=None:
            self.name=name
        if partialFilterExpression!=None:
            if isinstance(partialFilterExpression,PartialFilterExpression):
                self.partialFilterExpression=partialFilterExpression.__data__
        if sparse!=None:
            self.sparse=True

        self.expireAfterSeconds=10



class Index(object):
    def __init__(self,fields,options=None):
        # type: (dict, IndexOption) -> object
        self.fields=fields
        if isinstance(options,IndexOption):
            self.options=options


def create_model(name,indexes,fields):
    # type: (str, list, object) -> object
    if not isinstance(name,str) or not isinstance(name,unicode):
        raise Exception("'{0}' must be str or unicode")
    instance_model=ModelDefinition(name)
    global __models__
    if __models__==None:
        __models__={}
        __models__.update({
            name:instance_model
        })
    if isinstance(indexes,list):
        instance_model.set_indexes(indexes)


