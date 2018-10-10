from config import database, helpers, db_context
from ...api import common

import datetime
_hasCreated=False
helpers.extent_model(
            "HCSSYS_FunctionListLabel",
            "base",
            application=("text", True),
            function_id=("text", True),
            language=("text", True),
            default_name=("numeric"),
            custom_name=("text"),
            description=("bool"),
        )
def on_before_insert(data):
    pass

def on_before_update(data):
    pass

helpers.events("HCSSYS_FunctionListLabel").on_before_insert(on_before_insert).on_before_update(on_before_update)
def HCSSYS_FunctionListLabel():
    ret = db_context.collection("HCSSYS_FunctionListLabel")
    return ret