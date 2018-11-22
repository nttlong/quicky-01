from _ast import alias

from sqlalchemy.sql.functions import count
from  datetime import datetime
from . helpers import expr,validators
from . helpers import get_model,get_keys_of_model
from pymongo import MongoClient
from pymongo.errors import OperationFailure
import threading
import logging
import copy
import pymongo
import pytz
import sys
from . import exec_mode
from bson.codec_options import CodecOptions
from . import helpers
from . import dict_utils
from pymongo.client_session import ClientSession
_cache_create_key_for_collection=None
def __parse_set_to_project__(data):
    ret ={}
    import pymqr

    if isinstance(data,set):
        selectors = list(data)
        index = 0
        for item in selectors:
            if isinstance(item,pymqr.pydoc.Fields):
                if item.__dict__.has_key('__alias__'):
                    ret.update({
                        item.__dict__['__alias__']:pymqr.pydoc.get_field_expr(item)
                    })
                else:
                    ret.update({
                        pymqr.pydoc.get_field_expr(item,True):1
                    })
            elif type(item) in [str,unicode]:
                ret.update({
                    item: 1
                })
            else:
                raise Exception("params at {0} with data type {1} is invalid\n"
                                "The valid data type is 'str', 'unicode' or {2}".format(
                    index,type(item),pymqr.pydoc.Fields
                ))
        return ret



def get_current_schema():
    # type: () -> str
    """
    get current schema in theading
    :return:
    """
    if hasattr(threading.currentThread(),"tenancy_code"):
        return threading.currentThread().tenancy_code
    else:
        return None
logger = logging.getLogger(__name__)
_db={}
def extract_data(data):
    ret={}
    for key in data.keys():
        if key.find(".")>-1:
            items=key.split('.')
            if not ret.has_key(items[0]):
                ret.update({
                    items[0]:{}
                })
            val=ret[items[0]]
            for x in items[1:items.__len__()-1]:
                if not val.has_key(x):
                    val.update({
                        x:{}
                    })
                val=val[x]
            val.update({
                items[items.__len__() - 1]:data[key]
            })

        else:
            ret.update({
                key:data[key]
            })
    return ret
def get_dict_of_instance(ins):
    if ins.__dict__.items().__len__() ==0:
        return  None
    ret = {}
    for k,v in ins.__dict__.items():
        if hasattr(v,"__dict__"):
            ret.update({
                k:get_dict_of_instance(v)
            })
        else:
            ret.update({
                k: v
            })
    return ret
class QR():
    """
    Define queryable
    """

    def __init__(self,config = None):
        self.db = None
        self._entity = None
        self._codec_options = None
        if config != None:
            self.db=config["database"]
            self._codec_options=config["codec_options"]
    def collection(self,name):
        "get collection from database. including methods: find_one,find,get_list,get_item,where,entity,aggregate "
        if name==None or name=="":
            raise Exception("'name' can not be null or empty")
        return COLL(self,name)
    def get_collection_names(self):
        return list(self.db.collection_names())
class ENTITY():
    """
        Define entity
    """
    def __init__(self, qr,coll, name):
        # type:(QR,COLL,str)->NotImplemented
        """
        Create new entity instance
        :param qr:query
        :param coll:COLLECTION
        :param name:model name
        """
        self.name = ""
        self.qr = None
        self._data = {}
        self._action = None
        self._expr = None
        self.qr = qr
        self.name = name
        self._coll=coll
    def insert_one(self,*args,**kwargs):
        # type: (tuple,dict) -> ENTITY
        """
        Insert one item example insert_one(a=1)
        :param args:
        :param kwargs:
        :return:
        """
        if args==():
            self._data=kwargs
        else:
            if hasattr(args[0],"__dict__"):
                self._data = get_dict_of_instance(args[0])
            else:
                self._data = args[0]

        self._action="insert_one"

        return self
    def insert_many(self,data):
        # type: (tuple,dict) -> ENTITY
        """
        Insert many items
        :param data:
        :return:
        """
        self._action = "insert_many"
        self._data = data
        return self
    def update_one(self,data):
        # type: (dict) -> ENTITY
        """
        update one item
        :param data:
        :return:
        """
        if hasattr(data, "__dict__"):
            _data = get_dict_of_instance(data)
        else:
            _data = data
        self._action="update_one"
        if not self._data.has_key("$set"):
            self._data.update({
                "$set":_data
            })
        else:
            x=self._data["$set"]
            for key in data.keys():
                x.update({
                    key:_data[key]
                })
        return self
    def update_many(self,data,*params):
        # type: (tuple,dict) -> ENTITY
        """
        Update many items
        :param data:
        :param params:
        :return:
        """
        if hasattr(data, "__dict__"):
            _data = get_dict_of_instance(data)
        else:
            _data = data
        self._action = "update_many"
        if not self._data.has_key("$set"):
            self._data.update({
                "$set": _data
            })
        else:
            x = self._data["$set"]
            for key in _data.keys():
                x.update({
                    key: _data[key]
                })
        return self
    def push(self,data):
        """
        Push data into collection
        :param data:
        :return:
        """
        if hasattr(data, "__dict__"):
            _data = get_dict_of_instance(data)
        else:
            _data = data
        self._action = "update_many"
        if not self._data.has_key("$push"):
            self._data.update({
                "$push": _data
            })
        else:
            x = self._data["$push"]
            for key in _data.keys():
                x.update({
                    key: _data[key]
                })
        return self
    def pull(self,data):
        if hasattr(data, "__dict__"):
            _data = get_dict_of_instance(data)
        else:
            _data = data
        self._action = "update_many"

        if not self._data.has_key("$pull"):
            self._data.update({
                "$pull": _data
            })
        else:
            x = self._data["$pull"]
            for key in _data.keys():
                x.update({
                    key: _data[key]
                })
        return self
    def inc(self,data):
        if hasattr(data, "__dict__"):
            _data = get_dict_of_instance(data)
        else:
            _data = data
        self._action = "update_many"
        if not self._data.has_key("$inc"):
            self._data.update({
                "$inc": _data
            })
        else:
            x = self._data["$inc"]
            for key in _data.keys():
                x.update({
                    key: _data[key]
                })
        return self
    def dec(self,data):
        if hasattr(data, "__dict__"):
            _data = get_dict_of_instance(data)
        else:
            _data = data
        self._action = "update_many"
        if not self._data.has_key("$dec"):
            self._data.update({
                "$dec": _data
            })
        else:
            x = self._data["$dec"]
            for key in _data.keys():
                x.update({
                    key: _data[key]
                })
        return self
    def filter(self,expression,*args,**kwargs):
        """
        Create filter before update or delete
        :param expression:
        :param args:
        :param kwargs:
        :return:
        """
        self._expr = expression
        if type(expression) is str:
            self._expr = helpers.filter(expression,*args,**kwargs).get_filter()
        return self
    def delete(self):
        self._action="delete"
        return self
    def get_duplicate_error(self,ex):
        msg =ex.message
        return self.__get_duplicate_error_by_msg__(msg)

    def __get_duplicate_error_by_msg__(self, msg):
        start = msg.find(" index:") + " index:".__len__()
        end = msg.find(" dup key:", start)
        key = msg[start:end]
        key = key.replace(" ", "")
        __schema__ = self._coll.schema
        if __schema__ == None:
            __schema__ = get_current_schema()
        info = self.qr.db.get_collection(__schema__ + "." + self._coll.get_name()).index_information()
        fields = info[key]["key"]
        ret_fields = []
        for item in fields:
            ret_fields.append(item[0])
        return dict(
            error=dict(
                fields=ret_fields,
                code="duplicate"
            )
        )

    def commit(self,session = None):
        """
        Commit actio. Example; insert_many then commit, update or delete require filter before
        :return:
        """


        _id=None
        if session != None and not isinstance(session,ClientSession):
            raise (Exception("Session must be 'pymongo.client_session.ClientSession'"))
        if type(self._data) is dict:
            if self._data.has_key("$set"):
                _id=self._data["$set"].get("_id",None)
                for key in self._data["$set"].keys():
                    if (key[0:1]=="$" or key == "_id") and (key not in ["$push","$pull"]):
                        self._data["$set"].pop(key)
            else:
                for key in self._data.keys():
                    if (key[0:1]=="$" or key == "_id") and (key not in ["$push","$pull"]):
                        self._data.pop(key)



        _coll=self._coll.get_collection()
        model_events = helpers.events(self._coll._model.name)
        if self._action=="insert_one":
            ret_data={}

            try:
                self._data=extract_data(self._data)
                if model_events!=None:
                    for fn in model_events._on_before_insert:
                        fn(self._data)
                ret_validate_require=validators.validate_require_data(self._coll._model.name,self._data)
                if ret_validate_require.__len__()>0:
                    if exec_mode.get_mode() == "off":
                        return dict(
                            error=dict(
                                fields=ret_validate_require,
                                code="missing"
                            )
                        )
                    elif exec_mode.get_mode() =="on":
                        raise(Exception("Data is missing\n"
                                        "The missing data are below\n{0}".format(ret_validate_require)))
                    elif exec_mode.get_mode() == "return":
                        return self._data,dict(
                                fields=ret_validate_require,
                                code="missing"
                            ),"Miss require value when insert data"

                ret_validate_data_type=validators.validate_type_of_data(self._coll._model.name,self._data)
                if ret_validate_data_type.__len__()>0:
                    if exec_mode.get_mode() == "off":
                        return dict(
                            error=dict(
                                fields=ret_validate_data_type,
                                code="invalid_data"
                            )
                        )
                    elif exec_mode.get_mode() == "on":
                        raise (Exception("Data invalid, the invlid data are below\n {0}".format(ret_validate_data_type)))
                    elif exec_mode.get_mode() == "return":
                        return self._data,dict(
                                fields=ret_validate_data_type,
                                code="invalid_data"
                            )
                ret = _coll.insert_one(self._data,False,session)
                ret_data = self._data.copy()
                ret_data.update({
                    "_id": ret.inserted_id
                })
                self._action = None
                self._data = {}
                if exec_mode.get_mode() == "off":
                    return dict(
                        error=None,
                        data=ret_data
                    )
                elif exec_mode.get_mode() =="return":
                    return ret_data, None,"Insert data is successfull"
                else:
                    return ret_data
            except pymongo.errors.DuplicateKeyError as ex:
                ret_data= self.get_duplicate_error(ex)
                if exec_mode.get_mode() == "off":
                    ret_data.update({
                        "data": self._data
                    })
                    return ret_data
                elif exec_mode.get_mode() == "on":
                    raise (Exception("Data is duplicate, duplicate fields is in {0}".format(ret_data['error']['fields'])))
                elif exec_mode.get_mode() == "return":
                    return self._data, ret_data,"Data is duplicate, duplicate fields is in {0}".format(ret_data['error']['fields'])
            except Exception as ex:
                raise ex


        elif self._action=="insert_many":

            if model_events:
                for item in self._data:
                    for fn in model_events._on_before_insert:
                        fn(item)
            try:
                ret = _coll.insert_many(self._data)
                self._action = None
                ret_data=list(self._data)
                for x in ret_data:
                    x["_id"]=ret.inserted_ids[ret_data.index(x)]
                self._data = {}
                if exec_mode.get_mode()=="off":
                    return dict(
                        data=ret_data,
                        error=None
                    )
                if exec_mode.get_mode()=="on":
                    return ret_data
                if exec_mode.get_mode()=="return":
                    return ret_data,None,"Insert many is successful"
            except pymongo.errors.BulkWriteError as ex:
                error=dict(
                    code="system",
                    error=dict(
                        message=ex.message
                    )
                )
                _ex=ex
                _msg=None
                if hasattr(ex,'details') and ex.details.has_key('writeErrors') and ex.details['writeErrors'].__len__()>0:
                    if ex.details['writeErrors'][0].get('code',None)==11000:
                        error = self.__get_duplicate_error_by_msg__(ex.details['writeErrors'][0]['errmsg'])
                        _ex = Exception("Duplicate data")
                        setattr(_ex,"fields",error['error']['fields'])
                        _msg="insert many duplicate data"
                if exec_mode.get_mode() == "on":
                    raise _ex
                if exec_mode.get_mode() == "off":
                    return error
                if exec_mode.get_mode()=="return":
                    from . import fx_model
                    return self._data,fx_model.s_obj(error),_msg

            except Exception as ex:
                raise ex


        else:
            if self._expr==None:
                raise Exception("Can not modified data without using filter")
            if self._action=="update_one":
                try:
                    ret = _coll.update_one(self._expr,self._data)
                    self._expr=None
                    self._action = None
                    self._data = {}
                    if exec_mode.get_mode() == "off":
                        return self._data
                    return ret
                except Exception as ex:
                    if exec_mode.get_mode() == "off":
                        return self._data, None, ex
                    raise ex


            if self._action=="update_many":
                if not self._data.has_key("$set"):
                    self._data={
                        "$set":self._data
                    }
                _sub_action_validate_require = []

                _chk_data =self._data
                if _chk_data.has_key("$set"):
                    _chk_data =self._data["$set"]
                _sub_actions = [(k,v.keys()[0]) for k,v in _chk_data.items() if type(v) is dict and v!={} and k in ["$push","$inc","$dec"]]
                if model_events:
                    _c_data = self._data.get("$set", {})
                    for fn in model_events._on_before_update:
                        fn(_c_data)
                # v_data=self._data.get("$set",self._data.get("$push",self._data.get("$pull",None)))
                ret_validate_require =[]
                ret_validate_require = validators.validate_require_data(self._coll._model.name, _c_data, partial=True)
                validate_from_fields =[]
                for x, y in _sub_actions:
                    vlds = validators.validate_require_data_from_field(self._coll._model.name, _c_data[x], y)
                    ret_validate_require.extend(vlds)
                if ret_validate_require.__len__() > 0:
                    if exec_mode.get_mode() == "off":
                        return dict(
                            error=dict(
                                fields=ret_validate_require,
                                code="missing"
                            )
                        )
                    elif exec_mode.get_mode() == "on":
                        raise (Exception("Data is missing\n Fields is missing:\n {0}".format(ret_validate_require)))
                    elif exec_mode.get_mode() == "return":
                        return self._data,dict(
                                fields=ret_validate_require,
                                code="missing"
                            ),"Data is missing\n Fields is missing:\n {0}".format(ret_validate_require)

                ret_validate_data_type = validators.validate_type_of_data(self._coll._model.name, _c_data)
                if ret_validate_data_type.__len__() > 0:
                    if exec_mode.get_mode() == "off":
                        return dict(
                            error=dict(
                                fields=ret_validate_data_type,
                                code="invalid_data"
                            )
                        )
                    elif exec_mode.get_mode() == "on":
                        raise (Exception("Data is invalid\n Fields is missing:\n {0}".format(ret_validate_data_type)))
                    else:
                        return self._data,dict(
                                fields=ret_validate_require,
                                code="missing"
                            ),"Data is invalid\n Fields is missing:\n {0}".format(ret_validate_data_type)
                _x = {}
                for k, v in _c_data.items():
                    if k[0] == "$":
                        if _x.has_key(k):
                            for a, b in v.items():
                                _x[key].update({a: b})
                        else:
                            _x.update({k: v})
                    else:
                        if not _x.has_key("$set"):
                            _x.update({"$set": {}})
                        _x["$set"].update({k: v})
                _data = self._data.copy()
                try:

                    ret = _coll.update_many(self._expr,_x,False,None,False,None,session)
                    self._expr = None
                    self._action = None

                    self._data = {}
                    if exec_mode.get_mode() == "off":
                        return dict(
                            error=None,
                            data=ret
                        )
                    elif exec_mode.get_mode() == "return":
                        return _data,None,"Update is successfull"
                    else:
                        return _data

                except pymongo.errors.DuplicateKeyError as ex:
                    ret_data = self.get_duplicate_error(ex)
                    if exec_mode.get_mode() == "off":
                        ret_data.update({
                            "data": self._data
                        })
                    elif exec_mode.get_mode() == "on":
                        raise (Exception("Data is duplicate,\n"
                                         "Duplicate fields are below\n{0}".format(ret_data)))
                    elif exec_mode.get_mode() == "return":
                        return _data,ret_data,"Duplicate fields are below\n{0}".format(ret_data)
                    return ret_data
                except Exception as ex:
                    if exec_mode.get_mode() == "return":
                        return _data,ex,"Update data is error with unknown error"
                    else:
                        raise (ex)

            if self._action=="delete":
                _data = self._data.copy()
                ret = _coll.delete_many(self._expr,None,session)
                self._expr = None
                self._action = None
                self._data = {}
                try:
                    ret = { "deleted":ret.deleted_count}
                    if exec_mode.get_mode() == "off":
                        return ret
                    elif exec_mode.get_mode() == "return":
                        return ret,None,"Delete data is successfull"
                except Exception as ex:
                    if exec_mode.get_mode() == "return":
                        return _data,ex,"Delete data is error with unknown error"
                    else:
                        raise (ex)
class WHERE():
    """
    This class define where for Entity will be remove on the next version
    """
    def __init__(self, coll):
        self.name = ""
        self._coll = None
        self._where_ = {}
        self._entity = None
        self._coll = coll
        self.name=coll.name
        self._update_data ={}
    @property
    def cursor(self):
        return self._coll.get_collection().find(self._where_)
    @property
    def items(self):
        return list(self.cursor)
    @property
    def item(self):
        return self._coll.get_collection().find_one(self._where_)
    @property
    def objects(self):
        from fx_model import s_obj
        cursor =self.cursor
        continue_fetch = True
        while continue_fetch:
            try:
                yield s_obj(cursor.next())
            except StopIteration as ex:
                continue_fetch = False
    @property
    def object(self):
        from fx_model import s_obj
        item = self.item
        if item == None:
            return None
        else:
            return s_obj(item)
    def to_entity(self):
        if self._entity==None:
            self._entity=ENTITY(self._coll.qr,self._coll,self.name)
        return self._entity
    def where(self,expression,*args,**kwargs):
        from . import helpers
        entity = self.to_entity()
        unknown_fields = entity._coll._model.validate_expression(expression, None, *args, **kwargs)
        if unknown_fields.__len__() > 0:
            raise (Exception("What is bellow list of fields?:\n" + entity._coll.descibe_fields("\t\t", unknown_fields) +
                             " \n Your selected fields now is bellow list: \n" +
                             entity._coll.descibe_fields("\t\t\t", entity._coll._model.get_fields())))
        self._where_=helpers.filter(expression,*args,**kwargs).get_filter()
        return self
    def where_and(self,expression,*args,**kwargs):
        from . import helpers
        entity = self.to_entity()
        unknown_fields = entity._model.validate_expression(expression, None, *args, **kwargs)
        if unknown_fields.__len__() > 0:
            raise (Exception("What is bellow list of fields?:\n" + entity._coll.descibe_fields("\t\t", unknown_fields) +
                             " \n Your selected fields now is bellow list: \n" +
                             entity._coll.descibe_fields("\t\t\t", entity._coll._model.get_fields())))
        filter =helpers.filter(expression,*args,**kwargs).get_filter()
        if not self._where_.has_key("$and"):
            fx =self._where_
            self._where_ ={"$and":[fx,filter]}
        else:
            self._where_["$and"].append(filter)
        return self
    def where_or(self,expression, *args, **kwargs):
        from . import helpers
        entity = self.to_entity()
        unknown_fields = entity._model.validate_expression(expression, None, *args, **kwargs)
        if unknown_fields.__len__() > 0:
            raise (Exception("What is bellow list of fields?:\n" + entity._coll.descibe_fields("\t\t", unknown_fields) +
                             " \n Your selected fields now is bellow list: \n" +
                             entity._coll.descibe_fields("\t\t\t", entity._coll._model.get_fields())))
        if not self._where_.has_key("$or"):
            fx = self._where_
            self._where_ = {"$or": [fx, filter]}
        else:
            self._where_["$or"].append(filter)
        return self
    def set(self,*args,**kwargs):
        data = kwargs
        if args.__len__()>0:
            data = args[0]
        self._update_data.update(data)
        _data = {}
        for k,v in data.items():
            if type(v) is dict:
                _data.update({k:v})
            elif hasattr(v,"__to_dict__"):
                _data.update({k: v.__to_dict__()})
        return self
    def push(self,*args,**kwargs):
        import inspect
        _name = "$"+inspect.stack()[0][3]
        data = kwargs
        if args.__len__() > 0:
            data = args[0]

        _data = {}
        for k,v in data.items():
            if type(v) is dict:
                _data.update({k:v})
            elif hasattr(v,"__to_dict__"):
                _data.update({k: v.__to_dict__()})
            else:
                _data.update({k: v})

        self._update_data.update({
            _name:_data
        })
        return self
    def pull(self,expression,*args,**kwargs):
        import inspect
        _name = "$" + inspect.stack()[0][3]

        _data = helpers.filter(expression,*args,**kwargs).get_filter()

        def fix_eq(_data):
            if not type(_data) is dict:
                return _data
            if _data.keys()[0]=="$eq":
                return _data["$eq"]
            _pull_filter_ = {}
            for k, v in _data.items():
                if type(v) is dict and v.has_key("$eq"):
                    _pull_filter_.update({k: fix_eq(v["$eq"])})
                elif type(v) is list:
                    _pull_filter_.update({k:[fix_eq(x) for x in v]})
                else:
                    _pull_filter_.update({k: v})
            return _pull_filter_

        _pull_data_ = helpers.slice_key_of_dict(fix_eq(_data))



        if not self._update_data.has_key(_name):
            self._update_data.update({
                _name:{}
            })
        _pull_data_old = self._update_data[_name]

        _pull_data_= helpers.merge_dict(_pull_data_old,_pull_data_)
        self._update_data.update({
            _name: _pull_data_
        })
        return self
    def inc(self,*args,**kwargs):
        import inspect
        _name = "$" + inspect.stack()[0][3]
        data = kwargs
        if args.__len__() > 0:
            data = args[0]

        self._update_data.update({
            _name: data
        })
        return self
    def dec(self,*args,**kwargs):
        import inspect
        _name = "$" + inspect.stack()[0][3]
        data = kwargs
        if args.__len__() > 0:
            data = args[0]

        self._update_data.update({
            _name: data
        })
        return self
    def delete(self,session=None):
        if self._update_data =={}:
            return None
        if self._where_ == {}:
            raise (Exception("Canot not commit without where conditional"))
        entity = self.to_entity()
        entity._action = "delete"
        entity._expr = self._where_
        ret = entity.commit(session)
        return ret
    def commit(self,session = None):
        if self._update_data =={}:
            return None
        if self._where_ == {}:
            raise (Exception("Canot not commit without where conditional"))
        entity = self.to_entity()
        entity._data= self._update_data
        entity._action = "update_many"
        entity._expr = self._where_
        ret = entity.commit(session)
        return ret
class COLL():
    """
    Define a collection
    """
    def __init__(self,qr,name):
        # type: (QR,str) -> NotImplemented
        """
        Create instance of COLL
        :param qr:
        :param name:
        """
        self.name = ""
        self.qr = None
        self._where = None
        self._entity = None

        self._none_schema_name=name
        self._never_use_schema=False #do not use schema whenever extract database from mongodb

        self._model=get_model(name)
        self.schema=get_current_schema()
        self.session = None


        self.qr=qr
    def turn_never_use_schema_on(self):
        """
        This method will tell to database in qmongo never use schema whenever excute mongodb query
        :return:
        """
        self._never_use_schema=True
    def set_session(self,_session):
        # type: (ClientSession) -> COLL
        """
        Join this collection to session
        :param _session:
        :return:
        """


        if not isinstance(_session,ClientSession):
            raise (Exception("Session must be 'pymongo.client_session.ClientSession'"))
        self.session=_session
        return self
    def set_schema(self,schema_name):
        # type: (str) -> COLL
        """
        Change schema name before use any data operation
        :param schema_name:
        :return:
        """
        self.schema=schema_name
        return  self
    def descibe_fields(self,tabs,fields):
        """
        Return list of fields
        :param tabs:
        :param fields:
        :return:
        """
        _fields = ""
        for x in fields:
            _fields += tabs+ x + "\n"
        return  _fields
    def get_name(self):
        # type:() -> str
        """
        Get name of collection without schema
        :return:
        """
        return self._none_schema_name

    def get_collection_name(self):
        if self.schema == None:
            return self._none_schema_name
        if not self._never_use_schema or self.schema !=None or self.schema == "":
            return self.schema+"."+self._none_schema_name
        else:
            return self._none_schema_name
    def get_collection(self):
        # type: () -> pymongo.collection.Collection
        """
        get mongodb collection, before get this method will run create unique key script according to 'key' in model
        :return:
        """
        context = self.qr.db

        if context == None:
            try:
                import django_db
                self.qr.db = django_db.getdb()

            except Exception as ex:
                from . import db_context
                context = db_context.get_db_context()
                if context == None:
                    raise (Exception("Please use:\n"
                                     "import qmongo\n"
                                     "qmongo.set_db_context(host=..,port=..,user=..,password=..,name=...)\n"
                                     "or you can use bellow statement:\n"
                                     "qmongo.set_db_context(\"mongodb://{username}:{password}@{host}:{port}/{database name}[:{schema}]\")"))
        elif type(context) is pymongo.database.Database:
            self.qr.db = context
        else:
            self.qr.db = context.db
        if self.schema == None:
            from . db_context import get_schema
            self.schema = get_schema()
            if self.schema == None:
                raise (Exception("Please use:\n"
                                 "import qmongo\n"
                                 "qmongo.set_schema(schema_name)"))

        # if hasattr(self,"__create_mongodb_view__"):
        #     self.__create_mongodb_view__(self)
        #     delattr(self,"__create_mongodb_view__")

        global _cache_create_key_for_collection
        from . import qview
        if qview._cach_view.has_key(self._none_schema_name):
            qview._cach_view[self._none_schema_name].__create_as_view__(self.schema)
        if _cache_create_key_for_collection==None:
            _cache_create_key_for_collection={}
        ret_coll=None
        if self._never_use_schema or self.schema == None or self.schema == "":
            ret_coll = self.qr.db.get_collection(self._none_schema_name).with_options(codec_options=self.qr._codec_options)
        else:
            ret_coll=self.qr.db.get_collection(self.schema+"."+ self._none_schema_name).with_options(codec_options=self.qr._codec_options)
        key_info=get_keys_of_model(self._none_schema_name)
        if key_info["keys"]!=None  and not dict_utils.has_key(_cache_create_key_for_collection,self.get_collection_name()):
            for item in key_info["keys"]:
                keys=[]
                partialFilterExpression={}

                for field_name in item:

                    keys.append((field_name,pymongo.ASCENDING))
                    if(self._model.meta[field_name]=="text"):
                        partialFilterExpression.update({
                            field_name:{
                                "$type":"string"
                            }
                        })
                if keys.__len__() > 0:

                    try:
                        ret_coll.create_index(keys,
                                          unique=True,
                                          partialFilterExpression=partialFilterExpression)
                        has_create_index=True
                        # ret_coll.create_index(keys,
                        #                       unique=True)
                        # _cache_create_key_for_collection.update({
                        #     self.get_collection_name():True
                        # })
                    except Exception as ex:
                        if ex.code==85:
                            _cache_create_key_for_collection.update({
                                self.get_collection_name(): True
                            })

                        logger.error(ex)

        return ret_coll
    def find_one(self,exprression=None,*args,**kwargs):

        # type: (str,dict|tuple|int|bool|float|datetime|list) -> dict

        """find one item with conditional ex: find_one("Username={0}","admin"),
            find_one("Username='admin'"),
            find_one("Username=@username",username="admin")
         """
        if exprression==None:
            return self.get_collection().find_one()

        unknown_fields = self._model.validate_expression(exprression,None,*args,**kwargs)
        if unknown_fields.__len__() > 0:
            raise (Exception("What is bellow list of fields?:\n" + self.descibe_fields("\t\t", unknown_fields) +
                             " \n Your selected fields now is bellow list: \n" +
                             self.descibe_fields("\t\t\t", self._model.get_fields())))
        if type(exprression) is dict:
            ret = self.get_collection().find_one(exprression)
            return ret
        elif type(exprression) is tuple:
            ret = self.get_collection().find_one(exprression[0])
            return ret
        else:
            if type(args) is tuple and args.__len__()>0 and kwargs=={}:
                kwargs=args[0]
            filter = expr.parse_expression_to_json_expression(exprression, kwargs)
            ret=self.get_collection().find_one(filter)
            return ret
    def objects(self,exprression=None,*args,**kwargs):
        from . import fx_model
        iters= self.cursors(exprression,*args,**kwargs)
        continue_fetch = True
        while continue_fetch:
            try:
                item = iters.next()
                yield fx_model.s_obj(item)
            except StopIteration as ex:
                continue_fetch  = False

    def cursors(self,exprression = None,*args,**kwargs):
        # type: (str,dict|tuple|int|bool|float|datetime|list) -> dict

        """find and get a list of items item with conditional ex: find("Username={0}","admin"),
                    find("Username='admin'"),
                    find("Username=@username",username="admin")
                 """
        if exprression == None:
            return self.get_collection().find()
        unknown_fields = self._model.validate_expression(exprression, None, *args, **kwargs)
        if unknown_fields.__len__() > 0:
            raise (Exception("What is bellow list of fields?:\n" + self.descibe_fields("\t\t", unknown_fields) +
                             " \n Your selected fields now is bellow list: \n" +
                             self.descibe_fields("\t\t\t", self._model.get_fields())))
        if type(exprression) is dict:
            ret = self.get_collection().find(exprression)
            return ret
        elif type(exprression) is tuple:
            ret = self.get_collection().find(exprression[0])
            return ret
        else:
            from . import helpers
            ret = self.get_collection().find(helpers.filter(exprression, *args, **kwargs).get_filter())
            return ret
    def find(self,exprression,*args,**kwargs):
        # type: (str,dict|tuple|int|bool|float|datetime|list) -> dict

        """find and get a list of items item with conditional ex: find("Username={0}","admin"),
                    find("Username='admin'"),
                    find("Username=@username",username="admin")
                 """
        return list(self.cursors(exprression,*args,**kwargs))
    def get_list(self):
        # type: () -> list
        """
        get list of items from mongodb
        :return:
        """
        ret = self.get_collection().find()
        return list(ret)
    def get_objects(self):
        # type: () -> list
        """
        get list of items from mongodb
        :return:
        """
        from . import fx_model
        ret = self.get_collection().find()
        m= True
        while m:
            try:
                item = ret.next()
                yield fx_model.s_obj(item)
            except StopIteration as ex:
                m = False

    def get_item(self):
        # type : ()-> dict
        """
        Get one item from mongodb without filtering
        :return:
        """
        ret = self.get_collection().find_one()
        return ret
    def get_object(self):
        # type : ()-> dict
        """
        Get one item from mongodb and return object without filtering
        :return:
        """
        from . import fx_model
        ret = self.get_collection().find_one()
        if ret == None:
            return None
        ret_object = fx_model.s_obj(ret)

        return ret_object
    def where(self,exprression,*args,**kwargs):
        # type: (str,dict|tuple) -> COLL

        """Create filter expression before get data from mongo
            Ex:where("strLenCP(Username)<3").get_list(),
               where("strLenCP(Username)<@strong_number",strong_number=5).get_list()
               where("strLenCP(Username)<{0}",5).get_list()

        """
        if self._where==None:
            self._where=WHERE(self)
            self._where.where(exprression,*args,**kwargs)
        return self._where
    def entity(self):
        self.get_collection()
        if self._entity==None:
            self._entity=ENTITY(self.qr,self,self.name)
        return self._entity
    def aggregate(self):
        """create aggregate before create pipeline"""
        return AGGREGATE(self,self.qr,self.name,self.session)
    def insert_object(self,obj_item):
        from . import fx_model
        if not hasattr(obj_item,"__to_dict__"):
            raise (Exception("Insert object must have '__to_dict__()'"))
        return self.insert(obj_item.__to_dict__())
    def insert(self,*args,**kwargs):
        # type: (dict|tuple) -> dict

        """
        insert item into database
        :param args:
        :param kwargs:
        :return: dict including data has been inserted and error
        """
        if args.__len__()==1 and type(args[0]) is list:
            ac = self.entity().insert_many(args[0])
        else:
            ac=self.entity().insert_one(*args,**kwargs)
        ret=ac.commit(self.session)
        return ret
    def insert_one(self,*args,**kwargs):


        # type: (dict|tuple) -> dict

        """
        insert item into database
        :param args:
        :param kwargs:
        :return: dict including data has been inserted and error
        """
        if type(args) is tuple and args.__len__() >0:
            if hasattr(args[0],"__to_dict__"):
                _args = args[0].__to_dict__()
                ac = self.entity().insert_one(_args)
                ret = ac.commit(self.session)
                return ret
        ac=self.entity().insert_one(*args,**kwargs)
        ret=ac.commit(self.session)
        return ret
    def update_object(self,obj_item,filter,*args,**kwargs):
        if not hasattr(obj_item,"__to_dict__"):
            raise (Exception("update object must have '__to_dict__()'"))
        return self.update(obj_item.__to_dict__(),filter,*args,**kwargs)
    def update(self,data,filter,*args,**kwargs):
        # type: (dict,str,int|bool|datetime|float|dict|tuple|list) -> dict


        """
        Update data example: update({"password":"123"},"username=={0}","admin")
        :param data:dict data will be update
        :param filter:conditional text expression
        :param args:
        :param kwargs:
        :return: dict with data and error
        """
        unknown_fields = self._model.validate_expression(filter,None,*args,**kwargs)
        if unknown_fields.__len__() > 0:
            raise (Exception("What is bellow list of fields?:\n" + self.descibe_fields("\t\t", unknown_fields) +
                             " \n Your selected fields now is bellow list: \n" +
                             self.descibe_fields("\t\t\t", self._model.get_fields())))
        if type(args) is tuple and args.__len__()>0 and kwargs=={}:
            if hasattr(args[0],"__to_dict__"):
                kwargs=(args[0].__to_dict__())
                args =()
        ac=self.entity().filter(filter,*args,**kwargs)
        ac.update_many(data)
        ret=ac.commit(self.session)
        return ret

    def push_object(self, obj_item, filter, *args, **kwargs):
        if not hasattr(obj_item,"__to_dict__"):
            raise (Exception("push object must have '__to_dict__()"))
        return self.push(obj_item.__to_dict__(), filter, *args, **kwargs)
    def push(self,data,filter,*args,**kwargs):

        # type: (dict,str,int|bool|datetime|float|dict|tuple|list) -> dict


        """
        Update data example: update({"password":"123"},"username=={0}","admin")
        :param data:dict data will be update
        :param filter:conditional text expression
        :param args:
        :param kwargs:
        :return: dict with data and error
        """
        unknown_fields = self._model.validate_expression(filter,None,*args,**kwargs)
        if unknown_fields.__len__() > 0:
            raise (Exception("What is bellow list of fields?:\n" + self.descibe_fields("\t\t", unknown_fields) +
                             " \n Your selected fields now is bellow list: \n" +
                             self.descibe_fields("\t\t\t", self._model.get_fields())))
        if type(args) is tuple and args.__len__()>0 and kwargs=={}:
            kwargs=args[0]
            if hasattr(kwargs,"__to_dict__"):
                kwargs=(kwargs.__to_dict__())
        ac=self.entity().filter(filter,kwargs)
        ac.push(data)
        ret=ac.commit(self.session)
        return ret
    def pull(self,data,filter,*args,**kwargs):
        # type: (dict,str,int|bool|datetime|float|dict|tuple|list) -> dict


        """
        Update data example: update({"password":"123"},"username=={0}","admin")
        :param data:dict data will be update
        :param filter:conditional text expression
        :param args:
        :param kwargs:
        :return: dict with data and error
        """
        unknown_fields = self._model.validate_expression(filter,None,*args,**kwargs)
        if unknown_fields.__len__() > 0:
            raise (Exception("What is bellow list of fields?:\n" + self.descibe_fields("\t\t", unknown_fields) +
                             " \n Your selected fields now is bellow list: \n" +
                             self.descibe_fields("\t\t\t", self._model.get_fields())))
        ac=self.entity().filter(filter,kwargs)
        ac.pull(data)
        ret=ac.commit(self.session)
        return ret
    def create_unique_index(self,*args,**kwargs):
        """
        Create unique key refer to link : https://docs.mongodb.com/manual/reference/method/db.collection.createIndex/
        :param args:
        :param kwargs:
        :return:
        """
        if type(args) is tuple and args.__len__()>0:
            args=args[0]
        for item in args:
            keys=[]
            partialFilterExpression={}
            coll = self.get_collection()
            for x in item:
                keys.append((x["field"],pymongo.ASCENDING))
                partialFilterExpression.update({
                    x["field"]:{
                        "$type":x["type"]
                    }
                })

            # collation = pymongo.collation.Collation(locale=x["locale"], strength=2)
            coll.create_index(keys,
                              unique=True,

                              partialFilterExpression=partialFilterExpression)

        return self
    def delete(self,filter,*args,**kwargs):
        # type: (str,int|float|datetime|str|unicode|dict|tuple|str) -> dict

        """
        Delete data according to filter expression. Example detele("IsInactive=={0},True)
        :param filter:
        :param args:
        :param kwargs:
        :return:
        """
        unknown_fields = self._model.validate_expression(filter,None,*args,**kwargs)
        if unknown_fields.__len__() > 0:
            raise (Exception("What is bellow list of fields?:\n" + self.descibe_fields("\t\t", unknown_fields) +
                             " \n Your selected fields now is bellow list: \n" +
                             self.descibe_fields("\t\t\t", self._model.get_fields())))
        ac=self.entity().filter(filter,*args,**kwargs)
        ac.delete()
        ret=ac.commit(self.session)
        return ret
    def get_filter_keys(self,keys):
        ret=""
        for key in keys:
            ret+="("+key+"==@"+key+")and"
        return ret[0:ret.__len__()-3]
    def save(self,data,keys):
        _data = data
        if hasattr(data, "__to_dict__"):
            _data = data.__to_dict__()
        filter_key=self.get_filter_keys(keys)
        data_item=self.find_one(filter_key,_data)
        ret={}
        if data_item!=None:
            ret_val=self.update(data,filter_key,_data)
        else:
            ret_val=self.insert(_data)
        return ret_val
class AGGREGATE():
    """
    This class is a utility for mongodb aggregation framework. For more detail refer to :https://docs.mongodb.com/manual/aggregation/

    """

    def __init__(self,coll, qr, name,session = None):
        # type: (COLL,QR,str) -> AGGREGATE
        """
        Create instance of AGGREGATE
        :param coll: instance of COLL
        :param qr: instance of QR, this param will be use when get data from mongodb
        :param name: collecion name without schema
        """
        if session != None and not isinstance(session,ClientSession):
            raise (Exception("session must be 'pymongo.client_session.ClientSession'"))
        self.session=session
        self._coll=coll
        self._selected_fields = None
        self.qr = qr
        self.name = name
        self._pipe=[]
        self.full_fill = True
    def get_selected_fields(self):
        pass
        # # type: () -> list
        # """
        # Get current selected fields of aggregate pipeline
        # :return:
        # """
        # if self._selected_fields==None:
        #     self._selected_fields=self._coll._model.get_fields()
        #     if self._selected_fields.count("_id") == 0:
        #         self._selected_fields.append("_id")
        # ret =[]
        # for x in self._selected_fields:
        #     if ret.count(x) == 0:
        #         ret.append(x)
        # return ret
    def descibe_fields(self,tabs,fields):
        # type: (str,list) -> str
        """
        Create well form text for list of fields
        :param tabs: indent tab of each field must be a string contains only '\t'
        :param fields: list of fields
        :return: well form text
        """
        _fields = ""
        for x in fields:
            _fields += tabs+ x + "\n"
        return  _fields
    def check_fields(self,field):
        pass
        # # type: (str) -> bool
        # """
        # Check a field if it is in list of current selected fields
        # :param field:
        # :return: if field was found return True else False
        # """
        # ret=[x for x in self.get_selected_fields() if x==field]
        # return ret.__len__()>0

    def project(self,*args,**kwargs):
        # type: (dict|tuple) -> AGGREGATE

        """
        Create project pipeline (refer to :https://docs.mongodb.com/manual/reference/operator/aggregation/project/)
        Ex:
            project(
                dict(
                    FullName="toUpper(concat(FirstName,' ',LastName))",
                    Age="year(@time_now)- year(BirthDate)",
                    Username=1,
                    CreatedOn=1
                ),
                time_now=datetime.now()
            )
            or
            project (
                username=1,
                password=1,
                myConst="titeral(1)",
                total_salary="BasicSalary + MonthlySalary"
            )

        :param args:
        :param kwargs:
        :return:
        """
        _project = {}
        if kwargs=={}:
            kwargs = args[0]
            if args.__len__()>1:

                params=args[1]
            elif isinstance(args[0],set):
                self._pipe.append({
                    "$project": __parse_set_to_project__(args[0])
                })
                self.full_fill = False
                return self

            else:
                params = args[0]

        else:

            params=[]
            if type(args) is tuple and args.__len__()>1 and type(args[0]) is dict:

                params=[e for e in args if args.index(e)>0]
                kwargs = args[0]
                args=[]
            elif type(args) is tuple and args.__len__()==1 and type(args[0]) is dict:
                params=kwargs
                kwargs=args[0]
        _next_step_fields=[]
        __params__=[v for k,v in kwargs.items() if k=="__params__"]
        if __params__.__len__()>0:
            params = __params__[0]
        elif type(args) is tuple and args.__len__()>0:
            params =args[0]
        _tmp_ = {}
        for k,v in kwargs.items():
            if k !="__params__":
                _tmp_.update({k:v})
        kwargs =_tmp_


        for key in kwargs.keys():
            if key != "_id":
                if kwargs[key]==1:
                    _project.update({
                        key: 1
                    })
                else:
                    _project.update({
                        key: expr.get_calc_expr(kwargs[key],*params)
                    })
                    _next_step_fields.append(key)
            else:
                _project.update({
                    key: kwargs[key]
                })
        self._selected_fields=_next_step_fields
        self._pipe.append({
            "$project":_project
        })
        return self
    def group(self,_id,selectors,*args,**kwargs):
        # type: (dict,dict|tuple|dict) -> AGGREGATE

        """
        Create a group pipeline for mongodb aggregate (refer to: https://docs.mongodb.com/manual/reference/operator/aggregation/group/)
        Example: group(_id=dict(
                                month="month(MyDate)",
                                day="dayOfMonth(MydDate)",
                                year="year(MyDate)"),
                        selectors=dict(
                                   totalPrice="sum(price*quantity+{0})),
                                   12)

        :param _id:
        :param selectors:
        :param args:
        :param kwargs:
        :return:
        """
        _next_step_fields=[]
        __id={}
        if type(_id) is dict:
            for key in _id.keys():

                __id.update({
                    key:expr.get_calc_expr(_id[key],*args,**kwargs)
                })
        else:

            __id="$"+_id
            _next_step_fields.append("_id")

        _group = {
            "$group": {
                "_id": __id
            }
        }
        if not type(selectors) is dict:
            raise (Exception("'selectors' must be dict type"))


        for key in selectors.keys():
            _group["$group"].update({
                key:expr.get_calc_expr(selectors[key],*args,**kwargs)
            })
            _next_step_fields.append(key)
        self._selected_fields = _next_step_fields
        self._pipe.append(_group)
        return self
    def skip(self,len):
        # type: (int) ->AGGREGATE
        """
        Skip aggregate
        :param len:
        :return:
        """
        self._pipe.append({
            "$skip":len
        })
        return self
    def limit(self,num):
        # type: (int) ->AGGREGATE
        """
        Limit aggregate
        :param num:
        :return:
        """
        self._pipe.append({
            "$limit": num
        })
        return self

    def unwind(self,field_name,preserve_null_and_empty_arrays=True):
        # type: (str) -> AGGREGATE
        """
        Unwin aggregate
        :param field_name: the field name for "unwind" without prefix "$"
        :return:
        """
        import pymqr
        if isinstance(field_name,pymqr.pydoc.Fields):
            field_name = pymqr.pydoc.get_field_expr(field_name,True)
        if field_name[0:1]!="$":
            field_name="$"+field_name
        self._pipe.append({
            "$unwind":{"path":field_name,
                        "preserveNullAndEmptyArrays":preserve_null_and_empty_arrays
                    }
        })
        return self
    def match(self,expression, *args,**kwargs):
        # type: (str,int|bool|datetime|str|unicode|float|dict|tuple|list) -> AGGREGATE


        """
        Mathc aggregate Example:
            macth("userame=={0} and is_active=={1}",'admin',True)
        :param expression:
        :param args:
        :param kwargs:
        :return:
        """
        """Beware! You could not use any Aggregation Pipeline Operators, just use this function with Field Logic comparasion such as:
        and,or, contains,==,!=,>,<,..
        """
        import pymqr
        if isinstance(expression,pymqr.pydoc.Fields):
            self._pipe.append({
                "$match": pymqr.pydoc.get_field_expr(expression,True)
            })
            return self
        by_params=False
        # if args==():
        #     args=kwargs
        #     by_params=True

        if type(expression) is dict:
            self._pipe.append({
                "$match":expression
            })
            return self
        if type(expression) in [str,unicode]:
            import helpers
            self._pipe.append({
                "$match": helpers.filter(expression, *args,**kwargs)._pipe
            })
            return self


    def join(self,source,local_field,foreign_field,alias):
        self.lookup(source,local_field,foreign_field,alias)
        self.unwind(alias,False)
        return self
    def left_join(self,source,local_field,foreign_field,alias):
        self.lookup(source,local_field,foreign_field,alias)
        self.unwind(alias)
        return self
    def lookup(self,
               source=None,
               local_field=None,
               foreign_field=None,
               alias=None,
               *args,**kwargs):
        # type: (str|COLL,str,str,str) -> AGGREGATE
        """
        Create lookup aggregate
        :param source: where this collection will lookup for mongodb that is 'from'
        :param local_field:which is the field in this collection serve for lookup? for mongodb that is 'localField'
        :param foreign_field:which is the field from source collection serve for lookup? for mongodb that is 'foreignField'
        :param alias:The alias after lookup for mongdb that is 'as'
        :param args:
        :param kwargs:
        :return:
        """
        import pymqr
        if isinstance(local_field,pymqr.pydoc.Fields):
            local_field = pymqr.pydoc.get_field_expr(local_field,True)
        if isinstance(foreign_field,pymqr.pydoc.Fields):
            foreign_field = pymqr.pydoc.get_field_expr(foreign_field,True)
        if isinstance(alias,pymqr.pydoc.Fields):
            alias = pymqr.pydoc.get_field_expr(alias,True)



        if args==() and kwargs=={}:
            _source=source
            if source.__class__ is COLL:
                _source=source.get_collection_name()
            if hasattr(source,"coll"):
                _source = source.coll.get_collection_name()

            kwargs.update(source=_source,
                          local_field=local_field,
                          foreign_field=foreign_field,
                          alias=alias)
        else:
            if not dict_utils.has_key(kwargs,"source"):
                raise Exception("'source' was not found")
            if not dict_utils.has_key(kwargs,"local_field"):
                raise Exception("'local_field' was not found")
            if not dict_utils.has_key(kwargs,"foreign_field"):
                raise Exception("'foreign_field' was not found")
            if not dict_utils.has_key(kwargs,"alias"):
                raise Exception("'alias' was not found")
        source_model=None
        if isinstance(source,COLL):
            source_model =source._model
        elif hasattr(source,"coll"):
            source_model = source.coll._model

        else:
            source_model = get_model(source)


        self._pipe.append({
            "$lookup":{
                "from":kwargs["source"],
                "localField":kwargs["local_field"],
                "foreignField":kwargs["foreign_field"],
                "as":kwargs["alias"]
            }
        })
        return self
    def sort(self,*args,**kwargs):
        if args==() and kwargs=={}:
            raise (Exception("It look like you forgot set sort fields\nHow to sort?\n"
                             ".sort(\n"
                             "\tfield name=1 or -1\n,"
                             "\t..\n"
                             "\tfield name n=1 or -1"))
        _sort={

        }

        _sort = (lambda x, y: y if y != {} else x[0])(args, kwargs)
        self._pipe.append({
            "$sort":_sort
        })
        return self
    def count(self,alias):
        """
        Create count aggregate pipeline
        :param alias: Alias field will hold count value
        :return:
        """
        self._pipe.append({
            "$count":alias
        })
        return self
    def get_item(self):
        """
        Get one item from mongdb
        :return:
        """
        ret=self.get_list()
        if ret.__len__()==0:
            return None
        else:
            return ret[0]
    def get_object(self):
        from . import fx_model

        ret_item =self.get_item()
        if ret_item == None:
            return None
        ret= fx_model.s_obj(ret_item)
        # from . import dynamic_object
        # ret = dynamic_object.create_from_dict(self.get_item())
        return  ret

    def get_all_documents_as_objects(self):
        from . import fx_model
        """
        get all items from mongodb
        Caution: this method will return what is collection store. For example the collection maybe store different schema in each doc
        :return:
        """
        # coll = self.qr.db.get_collection(self.name).with_options(codec_options=self.qr._codec_options)
        coll = self._coll.get_collection()
        coll_ret = coll.aggregate(self._pipe)
        ret=coll.aggregate(self._pipe)
        continue_fetch =True

        while continue_fetch:
            try:
                yield  fx_model.s_obj(ret.next())
            except StopIteration as ex:
                continue_fetch =False

    def get_all_documents(self):
        # type: () -> list
        """
        get all items from mongodb
        Caution: this method will return what is collection store. For example the collection maybe store different schema in each doc
        :return:
        """
        # coll = self.qr.db.get_collection(self.name).with_options(codec_options=self.qr._codec_options)
        coll = self._coll.get_collection()
        coll_ret = coll.aggregate(self._pipe)
        ret=list(coll.aggregate(self._pipe))
        return ret
    def cursor_list(self):
        # type: () -> list
        """
        Get list of item in mongodb
        Caution: this method will return the same schema for each item even the collection contains different schema for each item
        :return:
        """
        # try:
        #     return self.qr.db.get_collection(self.name).aggregate(self._pipe,explain=False)["cursor"]["firstBatch"]
        # except Exception as ex:
        #     return list(self.qr.db.get_collection(self.name).aggregate(self._pipe))
        # coll=self.qr.db.get_collection(self.name).with_options(codec_options=self.qr._codec_options)
        coll = self._coll.get_collection()
        coll_ret = coll.aggregate(self._pipe, self.session,allowDiskUse=True)
        return coll_ret
    def get_objects(self):
        from . import fx_model
        iters = self.cursor_list()
        continue_fetch = True
        while continue_fetch:
            try:
                yield fx_model.s_obj(iters.next())
            except StopIteration as ex:
                continue_fetch =False


    def get_list(self):
        # type: () -> list
        """
        Get list of item in mongodb
        Caution: this method will return the same schema for each item even the collection contains different schema for each item
        :return:
        """
        # try:
        #     return self.qr.db.get_collection(self.name).aggregate(self._pipe,explain=False)["cursor"]["firstBatch"]
        # except Exception as ex:
        #     return list(self.qr.db.get_collection(self.name).aggregate(self._pipe))
        # coll=self.qr.db.get_collection(self.name).with_options(codec_options=self.qr._codec_options)
        coll = self._coll.get_collection()
        coll_ret=self.cursor_list()

        ret=[]
        if sys.version_info[0]<=2:
            return list(coll_ret)

        else:
            return list(coll_ret)


        # ret=list(coll.aggregate(self._pipe))
        self._pipe=[]
        self._selected_fields=[]
        return ret
    def get_page_of_objects(self,page_index,page_size):
        # type: (int,int) -> dict
        """
        get page of item according to page_index and page_size
        Caution: this method will return the same schema for each item even the collection contains different schema for each item
        :param page_index:
        :param page_size:
        :return: dict including: page_size, page_index, total_items, items
        """
        _tmp_pipe = [x for x in self._pipe]
        _count_pipe=[]
        if sys.version_info[0]<=2:
            _count_pipe=[x for x in self._pipe if self._pipe.index(x)<self._pipe.__len__() and x.keys()[0]!="$sort"]
        else:
            _count_pipe = [x for x in self._pipe if self._pipe.index(x) < self._pipe.__len__() and list(x.keys())[0] != "$sort"]
        self._pipe = _count_pipe
        _sel_fields=self._selected_fields
        total_items_agg=self.count("total_items")
        total_items=total_items_agg.get_item()
        self._selected_fields=_sel_fields
        self._pipe=_tmp_pipe
        items=self.skip(page_index*page_size).limit(page_size).get_objects()
        class ret_cls(object):
            pass
        ret_obj=ret_cls()
        ret_obj.page_size = page_size;
        ret_obj.page_index = page_index;
        ret_obj.total_items = (lambda x: x["total_items"] if x != None else 0) (total_items);
        ret_obj.items = items;
        return ret_obj
    def get_page(self,page_index,page_size):
        # type: (int,int) -> dict
        """
        get page of item according to page_index and page_size
        Caution: this method will return the same schema for each item even the collection contains different schema for each item
        :param page_index:
        :param page_size:
        :return: dict including: page_size, page_index, total_items, items
        """
        _tmp_pipe = [x for x in self._pipe]
        _count_pipe=[]
        if sys.version_info[0]<=2:
            _count_pipe=[x for x in self._pipe if self._pipe.index(x)<self._pipe.__len__() and x.keys()[0]!="$sort"]
        else:
            _count_pipe = [x for x in self._pipe if self._pipe.index(x) < self._pipe.__len__() and list(x.keys())[0] != "$sort"]
        self._pipe = _count_pipe
        _sel_fields=self._selected_fields
        total_items_agg=self.count("total_items")
        total_items=total_items_agg.get_item()
        self._selected_fields=_sel_fields
        self._pipe=_tmp_pipe
        items=self.skip(page_index*page_size).limit(page_size).get_list()
        return dict(
            page_size=page_size,
            page_index=page_index,
            total_items= (lambda x: x["total_items"] if x != None else 0) (total_items),
            items=items
        )
    def __copy__(self):
        ret=AGGREGATE(self.qr,self.name)
        ret._pipe=[x for x in self._pipe]
        return ret
    def copy(self):
        return self.__copy__()
    def replace_root(self,field):
        self.check_fields(field)

        self._pipe.append({
            "$replaceRoot":{"newRoot":(lambda x : "$"+x if x[0] != "$" else x)(field)}
        })
        return self
    def as_view(self,viewname):
        from . import qview
        ret = qview.create_mongodb_view(
            self,
            viewname
        )
        return ret
def connect(*args,**kwargs):
    """
    Create db instance <br/>
    Ex:query.get_query(host="ip address",\n
                        name="database name",\n
                        port=,\n
                        user=,\n
                        password=,\n
                        tz_aware=True/False,\n
                        timezone='refer to link https://en.wikipedia.org/wiki/List_of_tz_database_time_zones'\n
                        )\n
     \n Why 'tz_aware' is the most important for your mongodb connection?\n
     Please refer to http://api.mongodb.com/python/current/examples/datetimes.html\n
     If you are using Django framwork this information maybe in 'USE_TZ' of setting.py\n
      Why 'timezone' is the most important for your mongodb connection?\n
      Please refer to http://api.mongodb.com/python/current/examples/datetimes.html\n
       If you are using Django framwork this information maybe in 'USE_TZ' of setting.py\n

    """
    try:
        global _db
        if args.__len__()==1 and  type(args[0]) is pymongo.database.Database:
            db = args[0]
            host = db.client.address[0]
            port = db.client.address[1]
            name = db.name
            key = "host={0};port={1};name={2}".format(
                host,
                port,
                name
            )
            if not _db.has_key(key):
                version = db.eval("return db.version()")

                _db[key] = {
                    "database": db,
                    "codec_options": codec_options,
                    "version": version,
                    "versions": version.split('.')
                }
            return QR(_db[key])


        if args.__len__()==0:
            args=kwargs
        else:
            args=args[0]
        if not dict_utils.has_key(args,"host"):
            raise (Exception("This look like you forgot set 'host' param.\n Where is your mongodb hosting?"))
        if not dict_utils.has_key(args,"port"):
            raise (Exception("This look like you forgot set 'port' param.\n What is your mongodb port? Is it '27017'"))
        if not dict_utils.has_key(args,"name"):
            raise (Exception(
                "This look like you forgot set 'name' (The name of database) param.\n Which is your mongodb database?"))
        if dict_utils.has_key(args,"user") and args.get("user",None)!=None:
            if not dict_utils.has_key(args,"password") or args.get("password", "") == "":
                raise (Exception("This look like you forgot set 'user' and 'password' params.\n How is your mongodb authorization?"))

        key="host={0};port={1};name={2}".format(
            args["host"],
            args["port"],
            args["name"]
        )
        if not dict_utils.has_key(_db,key):
            cnn=MongoClient(
                host=args["host"],
                port=args["port"]
            )
            db=cnn.get_database(args["name"])
            if args["user"]!=None:
                db.authenticate(args["user"],args["password"])
            if args.get("tz_aware",False):
                codec_options = CodecOptions(
                    tz_aware=True,
                    tzinfo=pytz.timezone(args["timezone"])
                )
            else:
                codec_options = CodecOptions(
                    tz_aware=False
                )

            version=db.eval("return db.version()")

            _db[key]={
                "database":db,
                "codec_options":codec_options,
                "version":version,
                "versions":version.split('.')
            }
        return QR(_db[key])
    except OperationFailure as ex:
        logger.debug(ex)
        raise ex
    except Exception as ex:
        logger.debug(ex)
        raise (ex)
class GRIDFS(object):
    def __init__(self,db = None):
        self.__db__= db
        self.__where__ = None
    def __db_context__(self):
        if self.__db__ == None:
            from . import db_context
            context = db_context.get_db_context()
            if context == None:
                raise (Exception("Please use:\n"
                                 "import qmongo\n"
                                 "qmongo.set_db_context(host=..,port=..,user=..,password=..,name=...)\n"
                                 "or you can use bellow statement:\n"
                                 "qmongo.set_db_context(\"mongodb://{username}:{password}@{host}:{port}/{database name}[:{schema}]\")"))
            else:
                self.__db__ = context.db
        return self.__db__
    def put(self,filename,contentType,content,aliases=None,meta=None,*args,**kwargs):
        import gridfs
        fs = gridfs.GridFS(self.__db_context__())
        try:
            ret = fs.put(content,filename=filename,contentType=contentType,alias=aliases,meta=meta)
            if exec_mode.get_mode() == "off":
                return dict(
                    error=None,
                    data=ret
                )
            else:
                return ret, None
        except Exception as ex:
            if exec_mode.get_mode() == "off":
                return dict(
                    error = ex,
                    data = None
                )
            elif exec_mode.get_mode() == "on":
                raise ex
            elif exec_mode.get_mode() == "return":
                return None,ex
    def get_content_by_id(self,id):
        from bson import ObjectId
        import gridfs
        if type(id) in [str,unicode]:
            id = ObjectId(id)
        content = gridfs.GridFS(self.__db_context__()).get(id)
        return content
    def get_items(self):
        import  gridfs
        return gridfs.GridFS(self.__db_context__()).list()
    def where(self,expression,*args,**kwargs):
        ret  = GRIDFS(self.__db__)
        ret.__where__ = helpers.filter(expression,*args,**kwargs).get_filter()
        return ret
    @property
    def items(self):
        import gridfs
        return list(gridfs.GridFS(self.__db_context__()).find(self.__where__))
    @property
    def item(self):
        import gridfs
        return gridfs.GridFS(self.__db_context__()).find_one(self.__where__)
    def __iter__(self):
        return self.items
    def put_from_file(self,path,filename = None,meta=None):
        from mimetypes import MimeTypes
        import os
        mime = MimeTypes()
        with open(path,"r") as f:
            stm =f.read()
            import gridfs
            fs = gridfs.GridFS(self.__db_context__())
            try:
                if filename == None:
                    filename = os.path.basename(path)
                ret = fs.put(stm, filename=filename, contentType=mime.guess_type(path)[0],originalPath=path, meta=meta)
                if exec_mode.get_mode() == "off":
                    return dict(
                        error=None,
                        data=ret
                    )
                else:
                    return ret, None
            except Exception as ex:
                if exec_mode.get_mode() == "off":
                    return dict(
                        error=ex,
                        data=None
                    )
                elif exec_mode.get_mode() == "on":
                    raise ex
                elif exec_mode.get_mode() == "return":
                    return None, ex


