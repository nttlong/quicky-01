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
from . import fx_model
from . import helpers
from . import qview
from . import db_context
from . import auto_load_models as auto_loader
from . import exec_mode as exec_mode
set_except_mode = exec_mode.set_mode
get_except_mode = exec_mode.get_mode
from . exec_mode import exept_mode
define = helpers.define_model
extends = helpers.extent_model
extends_dict=helpers.extends_dict
view=qview.create_mongodb_view
view_from_pipe=qview.create_mongod_view_from_pipeline
models = fx_model.models
connect = db_context.connect
set_db_context = db_context.set_db_context
set_schema = db_context.set_schema
get_schema = db_context.get_schema
get_expr = helpers.expr.parse_expression_to_json_expression
selector = helpers.expr.get_calc_expr #make selector from expression
def create(*args,**kwargs):
    """Create new instance object from dict"""
    return fx_model.s_obj(*args,**kwargs)
