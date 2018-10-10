from config import database, helpers, db_context
from ...api import common

import datetime
_hasCreated=False
helpers.extent_model(
            "HCSSYS_Modules",
            "base",
            [['module_code']],
            module_code=("text", True),
            module_name=("text", True),
            module_type=("text"),
            url=("text"),
            redirect_url=("text"),
            sorting=("text"),
            is_new_tab=("bool")
        )
def on_before_insert(data):
    pass

def on_before_update(data):
    pass

helpers.events("HCSSYS_Modules").on_before_insert(on_before_insert).on_before_update(on_before_update)
def HCSSYS_Modules():
    ret = db_context.collection("HCSSYS_Modules")
    return ret