from config import database, helpers, db_context
from ...api import common

import datetime
_hasCreated=False
helpers.extent_model(
            "HCSLS_TrainField",
            "base",
            [['field_code']],
            field_code=("text", True),
            field_name=("text", True),
            field_name2=("text"),
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

helpers.events("HCSLS_TrainField").on_before_insert(on_before_insert).on_before_update(on_before_update)
def HCSLS_TrainField():
    ret = db_context.collection("HCSLS_TrainField")
    return ret