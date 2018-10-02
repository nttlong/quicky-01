from config import database, helpers, db_context
import datetime
helpers.extent_model(
            "auth_user_info",
            "base",
            [["login_account"], ["email"]],
            login_account = ("text",True),
            username=("text",True),
            display_name=("text",True),
            role_code=("text"),
            email=("text"),
            is_system=("bool"),
            never_expire=("bool"),
            manlevel_from=("numeric"),
            manlevel_to=("numeric"),
            mobile=("text"),
            description=("text"),
            created_on=("date"),
            created_by=("text"),
            modified_on=("date"),
            modified_by=("text")
        )
def auth_user_info():
    ret = db_context.collection("auth_user_info")
    return ret