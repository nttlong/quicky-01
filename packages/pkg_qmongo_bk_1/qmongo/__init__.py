VERSION = [1,0,0,"beta",10]
def get_version():
    return VERSION[0].__str__()+\
           "."+VERSION[1].__str__()+\
           "."+VERSION[2].__str__()+\
           "."+VERSION[3].__str__()+\
           "."+VERSION[4].__str__()

class _obj(object):
    pass
def create_object(*args,**kwargs):
    ret = _obj()
    data = {}
    if type(args) is tuple and args.__len__()>0:
        data = args[0]
    else:
        data = kwargs
    for k,v in data.items():
        if type(v) is dict:
            setattr(ret,k,create_object(v))
        else:
            setattr(ret, k, v)
    return ret
from . db_context import dbcontext
import fx_model
import helpers
import qview
import db_context
import auto_load_models as auto_loader
import exec_mode as exec_mode
set_except_mode = exec_mode.set_mode
get_except_mode = exec_mode.get_mode
from exec_mode import except_mode #set exception mode when mongodb commit to database
define = helpers.define_model
extends = helpers.extent_model
extends_dict=helpers.extends_dict
view=qview.create_mongodb_view
view_from_pipe=qview.create_mongod_view_from_pipeline
models = fx_model.models
connect = db_context.connect
set_db_context = db_context.set_db_context
get_db_context=db_context.get_db_context
set_schema = db_context.set_schema
get_schema = db_context.get_schema
get_expr = helpers.expr.parse_expression_to_json_expression
selector = helpers.expr.get_calc_expr #make selector from expression
lazyobject = fx_model.s_obj
def create(*args,**kwargs):
    """Create new instance object from dict"""
    return fx_model.s_obj(*args,**kwargs)
def grid_fs(db = None):
    from database import GRIDFS
    return GRIDFS(db)
global __schemas__
__schemas__ = []
class schema():
    def __init__(self,schema_name):
        self.__schema_name__ = schema_name
    def __enter__(self):
        __schemas__.append(get_schema())
        set_schema(self.__schema_name__)
    def __exit__(self, exc_type, exc_val, exc_tb):
        if __schemas__.__len__()>0:
            _c_schema_ = __schemas__.pop()
            set_schema(_c_schema_)
def call(functionName):
    from . import function_caller
    return function_caller.caller(functionName)
