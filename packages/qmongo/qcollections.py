"""
"NO_SQL":{
    "HOST":"192.168.18.43",
    "PORT":27017,
    "NAME":"lv_lms",
    "USER":"root",
    "PASSWORD":"123456"
  },
"""
from __builtin__ import property

from . fx_model import s_obj
from . import helpers
get_expression = helpers.expr.parse_expression_to_json_expression
__databases__ ={}
def connect(connection_name,host,port,name,user,password):
    if __databases__.has_key(connection_name):
        db = __databases__[connection_name]
    else:
        import pymongo
        cnn = pymongo.MongoClient(host=host,port=port)
        db=cnn.get_database(name)
        if db.authenticate(user,password):
            __databases__.update({connection_name:db})
    return db
def get_connect(connection_name):
    if __databases__.has_key(connection_name):
        return __databases__[connection_name]
    else:
        raise (Exception("'{0}' was not found, please use:\n"
                         "from qmongo import qcollection\n"
                         "qcollection.connect(connection name,host,port,database name, user, password)"))


class __aggregate__():
    def __init__(self,coll,pipeline,session):
        self.__coll__=coll
        self.__pipeline__ = pipeline
        self.__session__ = session
    def __fetch__(self,cursor):
        _continue_ =True
        while _continue_:
            try:
                item = cursor.next()
                yield s_obj(item)
            except StopIteration as ex:
                _continue_ = False
    @property
    def items(self):
        if self.__session == None:
            cursor = self.__coll__.aggregate(self.__pipeline)
        else:
            cursor = self.__coll__.aggregate(self.__pipeline,self.__session)
        return list(cursor)
    @property
    def objects(self):
        if self.__session__ == None:
            cursor = self.__coll__.aggregate(self.__pipeline__)
        else:
            cursor = self.__coll__.aggregate(self.__pipeline, self.__session__)
        return self.__fetch__(cursor)




class queryable(object):
    def __init__(self,*args,**kwargs):
        # import pymongo
        # if not type(coll) is pymongo.collection.Collection:
        #     raise (Exception("queryable must be init with  'pymongo.collection.Collection'"))
        # self.__coll__=coll
        self.__where__ = None
        self.__pipe_line__=[]
        self.__modifiers__={}
        self.__session__ = None
    @property
    def pipe_line(self):
        return self.__pipe_line__
    @property
    def collection_name(self):
        return self.__coll__.name
    @property
    def database(self):
        return self.__coll__.database
    def where(self,expression,*args,**kwargs):
        self.__where__ = get_expression(expression,*args,**kwargs)
        return self
    def __fetch__(self,cursor):
        _continue_ =True
        while _continue_:
            try:
                item = cursor.next()
                yield s_obj(item)
            except StopIteration as ex:
                _continue_ = False
    def find(self):
        if self.__where__ == None:
            cursor = self.__coll__.find()
            return self. __fetch__(cursor)
        else:
            cursor = self.__coll__.find(self.__where__)
            return self.__fetch__(cursor)
    @property
    def items(self):
        if self.__pipe_line__.__len__()>0:
            ret= self.aggregate.items
            self.clean
            return self
        if self.__where__ == None:
            cursor = self.__coll__.find()
            return list(cursor)
        else:
            cursor = self.__coll__.find(self.__where__)
            return list(cursor)
    @property
    def objects(self):
        if self.__pipe_line__.__len__()>0:
            ret = self.aggregate.objects
            self.clean
            return ret
        return list(self.find())
    @property
    def object(self):
        return s_obj(self.item)
    @property
    def item(self):
        if self.__pipe_line__.__len__()>0:
            self.limit(1)
            items =self.items
            self.clean
            if items.__len__()>0:
                return items[0]
            return None
        else:
            item =self.__coll__.find_one(self.__where__)
            return item

    def set_session(self,session):
        from pymongo.client_session import ClientSession
        if session != None and not isinstance(session,ClientSession):
            raise (Exception("Session must be 'pymongo.client_session.ClientSession'"))
        self.__session__ =session
        return self
    def insert(self,*args,**kwargs):
        items = kwargs
        if args.__len__()>0:
            items =args[0]
        if type(items) is list:
            lst = []
            for x in items:
                if type(x) is dict:
                    lst.append(x)
                elif hasattr(x,"__to_dict__"):
                    lst.append(x.__to_dict__())
            try:
                if self.__session__!=None:
                    ret=self.__coll__.insert_many(lst,self.__session__)
                else:
                    ret = self.__coll__.insert_many(lst)
                return ret,None
            except Exception as ex:
                return  None,ex
        elif type(items) is dict:
            try:
                if self.__session__ !=None:
                    ret =self.__coll__.insert_one(items,self.__session__)
                else:
                    ret = self.__coll__.insert_one(items)
                items.update({
                    "_id":ret.inserted_id
                })
                return items,None
            except Exception as ex:
                return items,ex
        elif hasattr(items,"__to_dict__"):
            try:
                ret =self.__coll__.insert_one(items.__to_dict__())
                items.__validator__ = False
                items._id=ret.inserted_id
                items.__validator__ = True
                return items,None
            except Exception as ex:
                return items,ex
    def set(self,*args,**kwargs):
        data = kwargs
        if args.__len__()>0:
            data = args[0]
        if not self.__modifiers__.has_key("$set"):
            self.__modifiers__.update({
                "$set":{}
            })
        for k,v in data.items():
            self.__modifiers__["$set"].update({
                k:v
            })
        return self
    def push(self,*args,**kwargs):
        data = kwargs
        if args.__len__() > 0:
            data = args[0]
        if not self.__modifiers__.has_key("$push"):
            self.__modifiers__.update({
                "$push": {}
            })
        for k, v in data.items():
            self.__modifiers__["$push"].update({
                k: v
            })
        return self
    def pull(self,expression,*args,**kwargs):
        from . import helpers
        data = kwargs
        if args.__len__() > 0:
            data = args[0]
        if not self.__modifiers__.has_key("$pull"):
            self.__modifiers__.update({
                "$pull": {}
            })
        cmp_expr = helpers.filter(expression,*args,**kwargs)
        for k,v in cmp_expr.items():
            self.__modifiers__["$push"].update({
                k:v
            })

        return self

    def commit(self):
        try:
            if self.__session__==None:
                ret = self.__coll__.update_many(self.__where__, self.__modifiers__)
            else:
                ret = self.__coll__.update_many(self.__where__, self.__modifiers__,self.__session__)
            return ret, None
        except Exception as ex:
            return None,ex
    @property
    def aggregate(self):
        return __aggregate__(self.__coll__,[x.copy() for x in self.__pipe_line__],self.__session__)
    @property
    def clean(self):
        self.__pipe_line__ =[]
        return self
    def project(self,*args,**kwargs):
        from . import helpers
        _project_={}
        data = kwargs
        params = []
        if args.__len__()>0:
            if type(args[0]) is list:
                params =args[0]
        for k,v in data.items():
            if v in [0,1]:
                _project_.update({k:v})
            elif type(v) in [str,unicode]:
                _project_.update({k: helpers.expr.get_calc_expr(v,*params)})
            elif type(v) is dict:
                _project_.update({k:v})
        self.__pipe_line__.append({"$project":_project_})
        return self
    def match(self,expression,*args,**kwargs):
        by_params = False
        if args == ():
            args = kwargs
            by_params = True
        from . import helpers
        if type(expression) is dict:
            self.__pipe_line__.append({
                "$match":expression
            })
            return self
        if type(expression) in [str,unicode]:
            import helpers
            self.__pipe_line__.append({
                "$match": (lambda :  helpers.filter(expression, args)._pipe if by_params else helpers.filter(expression, *args,**kwargs)._pipe)()
            })
            return self

    def skip(self,num):
        self.__pipe_line__.append({"$skip": num})
        return self
    def limit(self,num):
        self.__pipe_line__.append({"$limit": num})
        return self
    def __iter__(self):
        return self.objects
    def replace_root(self,field):
        self.__pipe_line__.append({
            "$replaceRoot": {"newRoot": (lambda x: "$" + x if x[0] != "$" else x)(field)}
        })
        return self
    def unwind(self,field,field_name,preserve_null_and_empty_arrays=True):
        self.__pipe_line__.append({
            "$unwind": {"path":(lambda x: "$" + x if x[0] != "$" else x)(field),
                        "preserveNullAndEmptyArrays":preserve_null_and_empty_arrays
                     }
        })
        return self
    def lookup(self,source,local_field,foreign_field,alias):
        self._pipe.append({
            "$lookup": {
                "from": source,
                "localField": local_field,
                "foreignField": foreign_field,
                "as": alias
            }
        })
        return self






























