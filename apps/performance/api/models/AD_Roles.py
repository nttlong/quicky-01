from config import database, helpers, db_context
import datetime
dict_permission = dict()
helpers.extent_model(
    "AD_Roles",
    "base",
    [["role_code"]],
    role_code = ("text",True),
    role_name=("text",True),
    dd_code=("text",True),
    description=("text"),
    stop=("bool"),
    #role_type=("text",True),
    #is_system=("bool"),
    #administrator=("numeric"),
    #system_admin=("numeric"),
    #function_admin=("text"),
    #security_level=("text"),
    #start_date=("date"),
    #end_date=("text"),
    #note=("date"),

    permission=("list", False, dict_permission.update({
        "function_id":("text"),
        "read":("text"), # Xem
        "create":("text"), # Them
        "write":("text"), # update
        "delete":("text"), # Xoa
        "export":("text"),
        "import":("text"),
        "copy":("text"),
        "attach":("text"),
        "download":("text"),
        "print":("text"),
        "action":("text"),
        "created_by":("text"),
        "created_on":("text"),
        "modified_by":("text"),
        "modified_on":("text")
        })),
    created_on=("date"),
    created_by=("text"),
    modified_on=("date"),
    modified_by=("text")
)

def AD_Roles():
    ret = db_context.collection("AD_Roles")
    return ret