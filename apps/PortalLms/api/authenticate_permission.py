import common
import datetime
import models

def get_permission(args):
    user_role = models.auth_user_info().aggregate().project(username = 1, role_code = 1)\
    .match("username == {0}", args['user'].username).get_item()
    ret = common.get_collection("AD_Roles").aggregate([
        {"$match": {
            "role_code": user_role.get('role_code', None)
        }},
        {"$unwind":{
            "path":"$permission",
            "preserveNullAndEmptyArrays":False
        }},
        {"$match":{
            "permission.function_id":args['data']['function_id']
        }},
        {"$project":{
            "_id":0,
            "function_id": "$permission.function_id",
            "read": "$permission.read",
            "create": "$permission.create",
            "write": "$permission.write",
            "delete": "$permission.delete",
            "export": "$permission.export",
            "import": "$permission.import",
            "copy": "$permission.copy",
            "attach": "$permission.attach",
            "download": "$permission.download",
            "print": "$permission.print",
            "action": "$permission.action"
        }}
    ])

    rs = list(ret)

    return (lambda x: x[0] if len(x) > 0 else {
        "function_id": args['data']['function_id'],
        "read": False,
        "create": False,
        "write": False,
        "delete": False,
        "export": False,
        "import": False,
        "copy": False,
        "attach": False,
        "download": False,
        "print": False,
        "action": False
    })(rs)
