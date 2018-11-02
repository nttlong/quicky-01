global __cnns__
global __schemas__
__cnns__ = []
__schemas__=[]
from . database import connect
from . database import QR
def set_db_context(*args,**kwargs):
    if args == () and kwargs == {}:
        raise (Exception("It lools like you forgot set arguments for 'set_db_context'\n"
                         "\tHow to use 'qmongo.db_context.set_db_context'?:\n"
                         "\t\t 1- qmongo.db_context.set_db_context('mongodb://<user>:<password>@<host>:<port>/<database>[:<schemma>]')\n"
                         "\t\t 2- qmongo.db_context.set_db_context(pymongo.database.Database instance)\n"
                         "\t\t 3- qmongo.db_context.set_db_context(db=pymongo.database.Database instance,schema='<schema name>')"))
    import threading
    import pymongo
    cnn = None

    if args == () and kwargs != {}:
        if kwargs.has_key("db") and type(kwargs["db"]) is pymongo.database.Database:
            cnn = QR()
            cnn.db = kwargs["db"]
            setattr(threading.currentThread(), "__qmongo_db_context_current_db", cnn)
        if kwargs.has_key("schema") and type("schema") in [str,unicode]:
            set_schema(kwargs["schema"])
        return cnn

    if type(args) is tuple and args.__len__()>0:
        if isinstance(args[0],QR):
            cnn= args[0]
        elif type(args[0]) is pymongo.database.Database:
            cnn = QR()
            cnn.db =args[0]
            setattr(threading.currentThread(), "__qmongo_db_context_current_db", cnn)
            return cnn


    if type(args[0]) in [unicode,str] and args[0][0:10] == "mongodb://":
        x= args[0]
        x = x[10:x.__len__()]
        if x.count("@") > 0:
            items = x.split("@")
            user_info = items[0].split(':')
            db_info = items[1].split('/')

            user = user_info[0]
            password = user_info[1]
            host_info = db_info[0].split(':')
            host = host_info[0]
            port = int(host_info[1])
            db_name = db_info[1]
            schema = None
            if db_info[1].count(':')>0:
                db_name = db_info[1].split(':')[0]
                schema  = db_info[1].split(':')[1]
            cnn = connect(
                host = host,
                port = port,
                user = user,
                password = password,
                name = db_name
            )
            if schema != None:
                set_schema(schema)


    if cnn == None:
        cnn = connect(*args, **kwargs)
    setattr(threading.currentThread(),"__qmongo_db_context_current_db",cnn)
    return cnn
def get_db_context():
    if hasattr(threading.currentThread(), "__qmongo_db_context_current_db"):
        return getattr(threading.currentThread(), "__qmongo_db_context_current_db")
    else:
        return None
import threading
def get_schema():
    "Get tenancy schema"
    if hasattr(threading.currentThread(),"tenancy_code"):
        return threading.currentThread().tenancy_code
    else:
        return None
def set_schema(schema):
    setattr(threading.currentThread(),"tenancy_code",schema)
    setattr(threading.current_thread(), "tenancy_code", schema)
def get_db_context():
    import threading
    if hasattr(threading.currentThread(), "__qmongo_db_context_current_db"):
        return threading.currentThread().__qmongo_db_context_current_db
    else:
        return None
class dbcontext():
    def __init__(self,*args,**kwargs):
        if args == () and kwargs == {}:
            raise (Exception("It lools like you forgot set arguments for 'set_db_context'\n"
                             "\tHow to use 'qmongo.db_context.set_db_context'?:\n"
                             "\t\t 1- qmongo.db_context.set_db_context('mongodb://<user>:<password>@<host>:<port>/<database>[:<schemma>]')\n"
                             "\t\t 2- qmongo.db_context.set_db_context(pymongo.database.Database instance)\n"
                             "\t\t 3- qmongo.db_context.set_db_context(db=pymongo.database.Database instance,schema='<schema name>')"))
        self.cnn =None
        self.schema = None
        if args.__len__() == 0:
            import pymongo
            from . import database
            if kwargs.has_key("schema"):
                self.schema = kwargs["schema"]
            if kwargs.has_key("db"):
                if isinstance(kwargs["db"], QR):
                    self.cnn = kwargs["db"]
                elif type(kwargs['db']) is pymongo.database.Database:
                    self.cnn = database.QR()
                    self.cnn.db = kwargs["db"]
        else:
            if type(args) is tuple and args.__len__() > 0:
                if isinstance(args[0], QR):
                    self.cnn = args[0]
            if type(args[0]) in [unicode, str] and args[0][0:10] == "mongodb://":
                x = args[0]
                x = x[10:x.__len__()]
                if x.count("@") > 0:
                    items = x.split("@")
                    user_info = items[0].split(':')
                    db_info = items[1].split('/')

                    user = user_info[0]
                    password = user_info[1]
                    host_info = db_info[0].split(':')
                    host = host_info[0]
                    port = int(host_info[1])
                    db_name = db_info[1]
                    schema = None
                    if db_info[1].count(':') > 0:
                        db_name = db_info[1].split(':')[0]
                        schema = db_info[1].split(':')[1]
                        self.cnn = connect(
                        host=host,
                        port=port,
                        user=user,
                        password=password,
                        name=db_name
                    )
                    if schema != None:
                        set_schema(schema)
            if self.cnn == None:
                self.cnn = connect(*args, **kwargs)


    def __enter__(self):
        db = get_db_context()
        if db != None:
            __cnns__.append(db)
        schema = get_schema()
        if schema!=None:
            __schemas__.append(schema)
        set_db_context(self.cnn)
        set_schema(self.schema)
    def __exit__(self, exc_type, exc_val, exc_tb):
        if __cnns__.__len__()>0:
            cnn = __cnns__.pop()
            set_db_context(cnn)
        if __schemas__.__len__()>0:
            schema = __schemas__.pop()
            set_schema(schema)

