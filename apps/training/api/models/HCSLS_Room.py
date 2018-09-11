from config import database, helpers, db_context
from ...api import common

import datetime
_hasCreated=False
helpers.extent_model(
            "HCSLS_Room",
            "base",
            [['room_code']],
            room_code=("text", True),
            room_name=("text", True),
            room_name2=("text"),
            supplier_code=("text"),
            room_map=("text"),
            ordinal=("numeric"),
            note=("text"),
            lock=("bool"),
            created_on=("date"),
            created_by=("text"),
            modified_on=("date"),
            modified_by=("text")
        )
def on_before_insert(data):
    pass

def on_before_update(data):
    pass

helpers.events("HCSLS_Room").on_before_insert(on_before_insert).on_before_update(on_before_update)
def HCSLS_Room():
    ret = db_context.collection("HCSLS_Room")
    return ret