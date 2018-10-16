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
from pymongo.database import Database
from pymongo.database import Collection
get_expression = helpers.expr.parse_expression_to_json_expression
global __databases__
__databases__ = {}
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
        if self.__session__ == None:
            cursor = self.__coll__.aggregate(self.__pipeline__)
        else:
            cursor = self.__coll__.aggregate(self.__pipeline__,self.__session__)
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
        from .database import QR
        import qmongo
        self.__coll__ = None

        if args ==() and kwargs == {}:
            raise (Exception("\n It look likes you forgot set params when call 'qcollections.queryable' \n"
                             "'qcollections.queryable' init with below option:\n"
                             "\t pymongo.database.Database -> db, str -> collection name\n"
                             "\t str - > db connection name,str - > collection name\n"
                             ""))
        self.__db__ = None
        if args.__len__()>0:
            if type(args[0]) is Database:
                self.__db__ =args[0]
                if args.__len__()>1 and type(args[1]) in [unicode,str]:
                    self.__coll__ = self.__db__.get_collection(args[1])
            if isinstance(args[0],QR):
                self.__db__ = args[0].db
            elif type(args[0]) is Collection:
                self.__coll__ = args[0]
            elif type(args[0]) in [unicode,str]:
                if not __databases__.has_key(args[0]) and isinstance(qmongo.get_db_context(),QR):
                    self.__db__ = qmongo.get_db_context().db
                if not __databases__.has_key(args[0]) and isinstance(qmongo.get_db_context(), Database):
                    self.__db__ = qmongo.get_db_context()
                elif qmongo.get_db_context()== None:
                    str_connections = ""
                    for k,v in __databases__.items():
                        str_connections = str_connections +"\n\t\t"+k
                    raise (Exception("It look likes you forgot call 'qcollections.connect' with connection name is'{0}'\n"
                                     "The database connection are in below list :{1}".format(args[0],str_connections)))
                elif __databases__.has_key(args[0]) and args.__len__()==2:
                    self.__db__ = __databases__[args[0]]
                    self.__coll__ = self.__db__.get_collection(args[1])
            if args.__len__()==2 and  self.__coll__ == None and type(args[1]) in [unicode,str]:
                self.__coll__ = self.__db__.get_collection(args[1])
            elif args.__len__()==1 and self.__coll__ == None and type(args[0]) in [unicode,str]:
                self.__coll__ = self.__db__.get_collection(args[0])
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
        try:
            self.__where__ = get_expression(expression,*args,**kwargs)
            self.__modifiers__ = {}
            return self
        except Exception as ex:
            raise (Exception("Error expression '{0}'".format(expression)))
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
            return ret
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
        if self.item == None:
            return  None
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
        if hasattr(data,"__to_dict__"):
            data = data.__to_dict__()
        if not self.__modifiers__.has_key("$set"):
            self.__modifiers__.update({
                "$set":{}
            })
        for k,v in data.items():
            if k != "_id":
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
                k.replace("[",".").replace("].","."): v
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
        _data = helpers.filter(expression, *args, **kwargs).get_filter()
        _pull_data = helpers.slice_key_of_dict(_data)
        _new_pull_ = helpers.merge_dict(self.__modifiers__["$pull"],_pull_data)
        self.__modifiers__["$pull"].update(_new_pull_)
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
        self.__where__ = None
        self.__pipe_line__ = []
        self.__modifiers__ = {}
        self.__session__ = None
        return self
    def new(self):
        self.__where__ = None
        self.__pipe_line__ = []
        self.__modifiers__ = {}
        self.__session__ = None
        return self
    def project(self,*args,**kwargs):
        from . import helpers
        _project_={}
        data = kwargs
        params = []
        if args.__len__()>0:
            if type(args[0]) is list:
                params =args[0]
        if args.__len__()>0 and type(args[0]) is dict:
            data=args[0]
            for i in range(1,args.__len__(),1):
                params.append(args[i])
        if args.__len__()==2 and type(args[0]) is list and type(args[1]) is dict:
            data = args[1]
            params =args[0]

        for k,v in data.items():
            if v in [0,1]:
                _project_.update({k:v})
            elif type(v) in [str,unicode]:
                _project_.update({k: helpers.expr.get_calc_expr(v,*params)})
            elif type(v) is dict:
                from . import q_dic_parse
                x= q_dic_parse.parse_to_mongo_dict(v,*params)
                if type(x) is dict:
                    for k1,v1 in x.items():
                        _project_.update({k+"."+k1:v1})
                else:
                    _project_.update({k: x})
            else:
                _project_.update({k: v})
        self.__pipe_line__.append({"$project":_project_})
        return self
    def add_fields(self,*args,**kwargs):
        from . import helpers
        _add_fields_ = {}
        data = kwargs
        params = []
        if args.__len__() > 0:
            if type(args[0]) is list:
                params = args[0]
        if args.__len__() > 0 and type(args[0]) is dict:
            data = args[0]
            for i in range(1, args.__len__(), 1):
                params.append(args[i])
        if args.__len__() == 2 and type(args[0]) is list and type(args[1]) is dict:
            data = args[1]
            params = args[0]

        for k, v in data.items():
            if v in [0, 1]:
                _add_fields_.update({k: v})
            elif type(v) in [str, unicode]:
                _add_fields_.update({k: helpers.expr.get_calc_expr(v, *params)})
            elif type(v) is dict:
                from . import q_dic_parse
                x = q_dic_parse.parse_to_mongo_dict(v, *params)
                if type(x) is dict:
                    for k1, v1 in x.items():
                        _add_fields_.update({k + "." + k1: v1})
                else:
                    _add_fields_.update({k: x})
            else:
                _add_fields_.update({k: v})
        self.__pipe_line__.append({"$addFields": _add_fields_})
        return self
    def create(self):
        ret= queryable({})
        return ret
    def coll_stats(self):
        self.__pipe_line__.append(
            { "$collStats": {"latencyStats": {"histograms": True}}}
        )
        return self
    def bucket_auto(self,group_by,buckets,ouput=None,params=[]):
        _output_ ={}
        if type(ouput) in [str,unicode]:
            _output_ = helpers.expr.get_calc_expr(_output_,*params)
        elif type(ouput) is dict:
            for k,v in ouput.items():
                if type(v) in [str,unicode]:
                    x = helpers.expr.get_calc_expr(v,*params)
                    _output_.update({
                        k: x
                    })
                elif type(v) is dict:
                    for k1,v1 in v.items():
                        _output_.update({
                            k + "." + k1: helpers.expr.get_calc_expr(v1,*params)
                        })
                else:
                    _output_.update({
                        k:v
                    })


        if ouput == None:
            self.__pipe_line__.append({
                "$bucketAuto":{
                    "groupBy":helpers.expr.get_calc_expr(group_by,params),
                    "buckets":buckets
                }
            })
        else:
            self.__pipe_line__.append({
                "$bucketAuto":{
                    "groupBy":helpers.expr.get_calc_expr(group_by,params),
                    "buckets":buckets,
                    "output":_output_
                }
            })


        return self

    def sort_by_count(self,field):
        self.__pipe_line__.append({
            "$sortByCount":"$"+field
        })
        return self

    def bucket(self,group_by,boundaries,default,output,params=[]):
        """
        groupBy: "$price",
                boundaries: [  0, 150, 200, 300, 400 ],
                default: "Other",
                output: {
                  "count": { $sum: 1 },
                  "titles": { $push: "$title" }
                }
        :return:
        """

        from . import q_dic_parse
        _output_ = {}
        for k,v in output.items():
            if type(v) in [str,unicode]:
                x=helpers.expr.get_calc_expr(v,params)
                _output_.update({
                    k: x
                })
            elif type(v) is dict:
                x = q_dic_parse.parse_to_mongo_dict(v,params)
                for k1,v1 in x.items():
                    _output_.update({
                        k+"."+k1: v1
                    })
            else:
                _output_.update({
                    k:v
                })
        _default_ = default
        if type(default) is dict:
            _default_ ={}
            for k,v in default.items():
                if type(v) is dict:
                    x= q_dic_parse.parse_to_mongo_dict(v,params)
                    for k1,v1 in x.items():
                        _default_.update({
                            k+"."+k1:v1
                        })
                else:
                    _default_.update(
                        {
                            k:v
                        }
                    )
        self.__pipe_line__.append({
            "$bucket":dict(
                groupBy="$"+group_by,
                boundaries =boundaries,
                default=_default_,
                output=_output_

            )
        })
        return self
    def facet(self,*args,**kwargs):
        data=kwargs
        if args.__len__() >0:
            data = args[0]
        _facet_ = {}
        for k,v in data.items():
            if type(v) is queryable:
                _facet_.update({
                    k:v.pipe_line
                })
            else:
                _facet_.update({
                    k:v
                })
        self.__pipe_line__.append({
            "$facet":_facet_
        })
        return self
    def redact(self,expression,*args,**kwargs):
        params= list(args)
        from . import helpers
        _redact_=helpers.expr.get_calc_expr(expression,*params)
        self.__pipe_line__.append({"$redact":_redact_})
        return self

    def out(self,to_collection_name):
        self.__pipe_line__.append({"$out": to_collection_name})
        return self
    def count(self,field):
        self.__pipe_line__.append({
            "$count":field
        })
        return self
    def match(self,expression,*args,**kwargs):
        from . import helpers
        if type(expression) is dict:
            self.__pipe_line__.append({
                "$match":expression
            })
            return self
        if type(expression) in [str,unicode]:
            import helpers
            self.__pipe_line__.append({
                "$match": helpers.filter(expression, *args,**kwargs)._pipe
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
    def unwind(self,field,preserve_null_and_empty_arrays=True):
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
    def group(self,_id,selectors,*args,**kwargs):
        from helpers import expr
        __id ={}

        if type(_id) is dict:
            for key,value in _id.items():
                __id.update({
                    key:expr.get_calc_expr(value,*args,**kwargs)
                })
        else:
            __id = "$" + _id
        _group = {
            "$group": {
                "_id": __id
            }
        }
        for key,value in selectors.items():
            _group["$group"].update({
                key:expr.get_calc_expr(value,*args,**kwargs)
            })
        self.__pipe_line__.append(_group)
        return self

    def sort(self,*args,**kwargs):
        import pymongo
        _sort_ = None

        if args.__len__()>0:
            _sort_ =args[0]
        else:
            _sort_ = kwargs

        _ret_sort= {}
        for k,v in _sort_.items():
            if v==1:
                _ret_sort.update({
                    k:pymongo.ASCENDING
                })
            else:
                _ret_sort.update({
                    k: pymongo.ASCENDING
                })
        self.__pipe_line__.append({
            "$sort": _ret_sort
        })
        return self
    def count_items(self):
        tmp = [x.copy() for x in self.__pipe_line__]
        self.__pipe_line__ =[]
        self.__pipe_line__.append({
            "$count": "count_items"
        })
        ret= self.object
        self.__pipe_line__ = tmp
        return ret.count_items

