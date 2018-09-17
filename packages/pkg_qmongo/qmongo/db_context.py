global __cnns__
global __schemas__
__cnns__ = []
__schemas__=[]
from . database import connect
from . database import QR
def set_db_context(*args,**kwargs):
    import threading
    cnn = None
    if type(args) is tuple and args.__len__()>0:
        if isinstance(args[0],QR):
            cnn= args[0]
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
    def __init__(self,schema=None,*args,**kwargs):
        self.cnn =None
        self.schema=schema
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

