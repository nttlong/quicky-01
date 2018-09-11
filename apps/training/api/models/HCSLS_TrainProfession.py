from config import database, helpers, db_context
from ...api import common

import datetime
_hasCreated=False
helpers.extent_model(
            "HCSLS_TrainProfession",
            "base",
            [['profession_code']],
            profession_code=("text", True),
            profession_name=("text", True),
            profession_name2=("text"),
            field_code=("text"),
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

helpers.events("HCSLS_TrainProfession").on_before_insert(on_before_insert).on_before_update(on_before_update)
def HCSLS_TrainProfession():
    ret = db_context.collection("HCSLS_TrainProfession")
    return ret