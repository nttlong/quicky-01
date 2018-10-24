import threading
from . import json_parser
class caller:
    def __init__(self,functionName):
        self.__functionName__=functionName
        self.__db__= None
    def params(self,*args,**kwargs):
        _param=kwargs
        if args.__len__()>0:
            _param=[]
            for item in args:
                if type(item) is dict:
                    _param.append(json_parser.to_json(item))
                else:
                    import json
                    _param.append(json.dumps(item))

        self.__params__=_param
        return self
    def get_command(self):
        ret = self.__functionName__
        ret=ret+"("+",".join(self.__params__)+")"
        return ret

    def set_database(self,db):
        self.__db__=db
        return self
    @property
    def items(self):
        if self.__db__ == None:
            from . import db_context
            db = db_context.get_db_context()
            from . import database
            if isinstance(db,database.QR):
                db=db.db
            self.__db__ = db
        ret=self.__db__.eval(self.get_command())
        if ret.has_key("_batch"):
            return ret["_batch"]
        return ret
    @property
    def result(self):
        if self.__db__ == None:
            from . import db_context
            db = db_context.get_db_context()
            from . import database
            if isinstance(db,database.QR):
                db=db.db
            self.__db__ = db
        ret = self.__db__.eval(self.get_command())
        if type(ret) is dict:
            from . import lazyobject
            return lazyobject(ret)
        else:
            return ret
    @property
    def objects(self):
        ret = self.items
        if type(ret) is list:
            for item in ret:
                from . import lazyobject
                yield  lazyobject(item)



