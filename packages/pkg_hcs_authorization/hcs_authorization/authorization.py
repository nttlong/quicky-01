from django.http import HttpResponse
import quicky
from quicky import JSON
from qmongo import database
Database = None
db_context=None
import action_type

def set_db_context_authorization(db_info):
    global Database
    global db_context
    Database = db_info
    db_context = database.connect(Database)

def get_collection(col_name):
    global db_context
    return db_context.db.get_collection(quicky.tenancy.get_schema() + "." + col_name)

def check_permission(function_id, username, act):
    user_role = db_context.collection("auth_user_info").aggregate().project(
        username = 1,
        role_code = 1
    ).match("username == {0}", username).get_item()

    if user_role == None or user_role == {}:
        return False

    qr = get_collection('AD_Roles').aggregate([
        {'$match': {'role_code': user_role.get('role_code', None)}},
        {'$unwind':{
            'path':'$permission',
            'preserveNullAndEmptyArrays':False
        }},
        {'$match':{
            '$expr':{
                '$eq': ['$permission.function_id', function_id]
            }
        }},
        {'$project':{
            "_id":0,
            "read":{ "$ifNull": [ "$permission.read", False ] },
            "create":{ "$ifNull": [ "$permission.create", False ] },
            "write":{ "$ifNull": [ "$permission.write", False ] },
            "delete":{ "$ifNull": [ "$permission.delete", False ] },
            "export":{ "$ifNull": [ "$permission.export", False ] },
            "import":{ "$ifNull": [ "$permission.import", False ] },
            "copy":{ "$ifNull": [ "$permission.copy", False ] },
            "attach":{ "$ifNull": [ "$permission.attach", False ] },
            "download":{ "$ifNull": [ "$permission.download", False ] },
            "print": { "$ifNull": [ "$permission.print", False ] },
            "action": { "$ifNull": [ "$permission.action", False ] }
        }}
    ])

    action = list(qr)
    if len(action) == 0:
        return False

    action = action[0]

    if act == action_type.Action.READ:
        return action['read']
    elif act == action_type.Action.ACTION:
        return action['action'] and action['read']
    elif act == action_type.Action.COPY:
        return action['copy'] and action['read']
    elif act == action_type.Action.CREATE:
        return action['create'] and action['read']
    elif act == action_type.Action.DELETE:
        return action['delete'] and action['read']
    elif act == action_type.Action.DOWNLOAD:
        return action['download'] and action['read']
    elif act == action_type.Action.EXPORT:
        return action['export'] and action['read']
    elif act == action_type.Action.IMPORT:
        return action['import'] and action['read']
    elif act == action_type.Action.PRINT:
        return action['print'] and action['read']
    elif act == action_type.Action.UPLOAD:
        return action['upload'] and action['read']
    elif act == action_type.Action.WRITE:
        return action['write'] and action['read']
    else:
        return False

def authorise_decorate(fn):
    def layer(*args, **kwargs):
        def repl(f):
            return fn(f, *args, **kwargs)
        return repl
    return layer

@authorise_decorate
def authorise(fn,*args,**kwargs):
    def wrapper(param):
        if kwargs.has_key('common') and kwargs['common'] == True:
            return fn(param)
        elif kwargs.has_key('action'):
            if(param['request'].META.has_key('HTTP_FUNCTION')):
                if check_permission(param['request'].META['HTTP_FUNCTION'], param['user'].username, kwargs['action']):
                    return fn(param)
        return HttpResponse(JSON.to_json({"error":"Unauthorized"}), status=401)
    return wrapper