from config import database, helpers, db_context
import datetime
helpers.extent_model(
            "auth_user",
            "base",
            [["username"]],
            username=("text",True),
            first_name=("text"),
            last_name=("text"),
            is_active=("bool"),
            email=("text"),
            is_superuser=("bool"),
            is_staff=("bool"),
            last_login=("date"),
            password=("text"),
            date_joined=("date")
        )
def auth_user():
    ret = db_context.collection("auth_user")
    return ret