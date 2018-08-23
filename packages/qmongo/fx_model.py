from bson.codec_options import CodecOptions

class s_obj_views(object):
    def __init__(self,owner):
        self.owner = owner
    def __getattr__(self, name):
        from . import qview
        return qview.create_mongodb_view(
            self.owner.aggregate,
            name
        )


class s_obj(object):
    pass
models = s_obj()
class __obj_fields__(object):
    def __init__(self,name = None,type = None, is_require = False):
        self.__name__ = name
        self.__type__= type
        self.__require__=is_require
    def __mk_obj__(self,item = None):
        ret = s_obj()
        if item == None:
            item =self
        for k,v in item.__dict__.items():
            if isinstance(v,__obj_fields__):
                if v.__type__ =="list":
                    setattr(ret,k,[])
                elif v.__type__ =="object":
                    if type(v) is __obj_fields__:
                        setattr(ret,k,v.__mk_obj__())
                    else:
                        setattr(ret, k, self.__mk_obj__(v))
                else:
                    setattr(ret, k, None)
            else:
                setattr(ret, k, None)
        return ret


class __obj_model__(object):
    def __init__(self,name,schema = None):
        _schema = models
        if schema != None:
            if not hasattr(models,schema):
                _schema = s_obj()
                setattr(models, schema, _schema)
            else:
                schema = getattr(models,schema)
        setattr(_schema,name,self)
        self.__name__=name
        self.__QR__ = None
        self.fields = __obj_fields__()
        self.__aggregate__=None
        # self.views = s_obj_views(self)
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
                    if type(v) is __obj_fields__:
                        setattr(ret,k,v.__mk_obj__())
                    else:
                        setattr(ret, k, self.mk_obj(v))
                else:
                    setattr(ret, k, None)
            else:
                setattr(ret, k, None)
        return ret
    @property
    def coll(self,context = None):
        from . import database

        ret = database.QR()
        # ret.db = context.db
        # ret._codec_options = CodecOptions()
        return ret.collection(self.__name__)
    @property
    def objects(self,filter = None,*args,**kwargs):
        if filter == None:
            return self.coll.get_objects()
        ret = self.coll.objects(filter,*args,**args)
        self.reset
        return ret
    def set_session(self,session):
        self.coll.set_session(session)
        return self
    @property
    def reset(self):
        self.__aggregate__ = None
        return self
    @property
    def aggregate(self):
        if self.__aggregate__ == None or self.__aggregate__.get_selected_fields() == [] :
            self.__aggregate__ =self.coll.aggregate()
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
        return self
    def insert(self,*args,**kwargs):
        ret = self.coll.insert(*args,**kwargs)
        import dynamic_object
        ret_obj = dynamic_object.create_from_dict(ret)
        ret_obj.is_error =False
        if ret.has_key("error"):
            ret_obj.is_error = True
            ret_obj.error_message = "insert data errror '{0}'".format(ret["error"]["code"])
        return ret_obj
    def insert_one(self,*args,**kwargs):
        ret = self.coll.insert_one(*args,**kwargs)
        import dynamic_object
        ret_obj = dynamic_object.create_from_dict(ret)
        ret_obj.is_error = False
        if ret.get("error",None) != None :
            ret_obj.is_error = True
            ret_obj.error_message = "insert data errror '{0}'".format(ret["error"]["code"])
        return ret_obj
    def update(self,data,*args,**kwargs):
        ret = self.coll.update(data,*args,**kwargs)
        import dynamic_object
        ret_obj = dynamic_object.create_from_dict(ret)
        ret_obj.is_error = False
        if ret.get("error", None) != None:
            ret_obj.is_error = True
            ret_obj.error_message = "insert data errror '{0}'".format(ret["error"]["code"])
        return ret_obj
    def delete(self,expression,*arg,**kwargs):
        ret = self.coll.delete(expression,*arg,**kwargs)
        import dynamic_object
        ret_obj = dynamic_object.create_from_dict(ret)
        ret_obj.is_error = False
        if ret.get("error", None) != None:
            ret_obj.is_error = True
            ret_obj.error_message = "insert data errror '{0}'".format(ret["error"]["code"])
        return ret_obj
    def find(self,expression,*args,**kwargs):
        return self.coll.find(expression,*args,**kwargs)
    def replace_root(self,field):
        self.aggregate.replace_root(field)
        return self
    def unwind(self,field,preserve_null_and_empty_arrays=True):
        """exce mongodb unwind"""
        self.aggregate.unwind(field,preserve_null_and_empty_arrays)
        return self
    @property
    def object(self):
        ret = self.aggregate.get_object()
        self.reset
        return ret
    def sort(self, *args, **kwargs):
        self.aggregate.sort(*args, **kwargs)
        return self
    def check_field(self,field):
        self.aggregate.check_fields(field)
        return self
    def count(self,alais = None):
        if alais == None:
            alais = self.__name__+"_____count"
        ret = self.aggregate.count(alais)
        self.reset
        return ret
    def skip(self,len):
        self.aggregate.skip(len)
        return self
    @property
    def cursors(self):
        ret = self.aggregate.cursor_list()
        self.reset
        return ret
    @property
    def item(self, *args, **kwargs):
        ret = self.aggregate.get_item()
        self.reset
        return ret
    @property
    def documents(self):
        ret = self.aggregate.get_all_documents()
        self.reset
        return ret
    @property
    def items(self):
        ret = self.aggregate.get_list()
        self.reset
        return ret
    def save(self,obj_item):
        """
        Save item arcoding to _id field value
        :param obj_item:
        :return:
        """
        if type(obj_item) is dict:
            find_item = self.coll.find_one("_id=={0}",obj_item["_id"])
            if find_item != None:
                ret = self.coll.update(obj_item,"_id=={0}",obj_item["_id"])
            else:
                ret = self.coll.insert_one(obj_item)
            return ret
        else:
            from . import dynamic_object
            item = dynamic_object.convert_to_dict(obj_item)
            find_item = self.coll.find_one("_id=={0}", item["_id"])
            if find_item != None:
                ret = self.coll.update(item,"_id=={0}",item["_id"])
                ret_object = dynamic_object.create_from_dict(ret)
                if ret.get("error",None) != None:
                    setattr(ret_object,"error_message","Update data error, error code is '{0}".format(ret["error"]["code"]))
                return ret_object
            else:
                ret = self.coll.insert_one(item)
                ret_object = dynamic_object.create_from_dict(ret)
                if ret.get("error",None) != None:
                    setattr(ret_object,"error_message","Insert data error, error code is '{0}".format(ret["error"]["code"]))
                return ret_object



