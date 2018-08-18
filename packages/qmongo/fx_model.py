from bson.codec_options import CodecOptions
class s_obj(object):
    pass
models = s_obj()
class __obj_fields__(object):
    def __init__(self,name = None,type = None, is_require = False):
        self.__name__ = name
        self.__type__= type
        self.__require__=is_require


class __obj_model__(object):
    def __init__(self,name):
        setattr(models,name,self)
        self.__name__=name
        self.__QR__ = None
        self.fields = __obj_fields__()
        self.__aggregate__=None
    def __create_field__(self,name,type="text",is_require=False):
        names = name.split('.')
        if not hasattr(self.fields,names[0]):
            setattr(self.fields,names[0],__obj_fields__(names[0],type,is_require))
        f = getattr(self.fields,names[0])
        if names.__len__() == 1:
            f.__type__ = type
        p = getattr(self.fields,names[0])
        str_name = names[0]
        for i in range(1,names.__len__()):
            if f.__type__ not in ["list","object"]:
                f.__type__ == "object"
            str_name = str_name + "." + names[i]
            if not hasattr(f, names[i]):
                setattr(f,names[i],__obj_fields__(str_name,type,is_require))
            f = getattr(f, names[i])
        return self
    def mk_obj(self,item = None):
        ret = s_obj()
        if item == None:
            item =self.fields
        for k,v in item.__dict__.items():
            if isinstance(v,__obj_fields__):
                if v.__type__ =="list":
                    setattr(ret,k,[])
                elif v.__type__ =="object":
                    setattr(ret,k,self.mk_obj(v))
                else:
                    setattr(ret, k, None)
            else:
                setattr(ret, k, None)
        return ret
    @property
    def query(self,context = None):
        if context == None:
            from . import db_context
            context = db_context.get_db_context()
        if context == None:
            raise (Exception("Please use:\n"
                             "import qmongo\n"
                             "qmongo.set_db_context(host=..,port=..,user=..,password=..,name=..."))
        from . import database

        ret = database.QR()
        ret.db = context.db
        ret._codec_options = CodecOptions()
        return ret.collection(self.__name__)
    @property
    def objects(self,filter = None,*args,**kwargs):
        return self.query.objects(filter,*args,**args)
    def set_session(self,session):
        self.query.set_session(session)
        return self
    @property
    def aggregate(self):
        if self.__aggregate__ == None:
            self.__aggregate__ =self.query.aggregate()
        return self.__aggregate__
    def project(self,*args,**kwargs):
        self.aggregate.project(*args,**kwargs)
        return self
    def lookup(self,source,local_field,foreign_field,alias):
        self.aggregate.lookup(source.__name__,local_field,foreign_field, alias)
        return self
    def join(self,source,local_field,foreign_field, alias):
        self.aggregate.join(source.__name__,local_field,foreign_field, alias)
        return self
    def left_join(self,source,local_field,foreign_field, alias):
        self.aggregate.left_join(source.__name__,local_field,foreign_field, alias)
    def insert(self,*args,**kwargs):
        return self.query.insert(*args,**kwargs)
    def insert_one(self,*args,**kwargs):
        return self.query.insert_one(*args,**kwargs)
    def update(self,data,*args,**kwargs):
        return self.query.update(data,*args,**kwargs)
    def delete(self,expression,*arg,**kwargs):
        return self.query.delete(expression,*arg,**kwargs)
    def find(self,expression,*args,**kwargs):
        return self.query.find(expression,*args,**kwargs)
    @property
    def object(self):
        return self.aggregate.get_object()
    def sort(self, *args, **kwargs):
        self.aggregate.sort(*args, **kwargs)
        return self
    def check_field(self,field):
        self.aggregate.check_fields(field)
        return self
    def count(self,alais = None):
        if alais == None:
            alais = self.__name__+"_____count"
        return self.aggregate.count(alais)
    def skip(self,len):
        self.aggregate.skip(len)
        return self
    @property
    def cursors(self):
        return self.aggregate.cursor_list()
    @property
    def item(self, *args, **kwargs):
        return self.aggregate.get_item()
    @property
    def documents(self):
        return  self.aggregate.get_all_documents()
    @property
    def items(self):
        return self.aggregate.get_list()



















