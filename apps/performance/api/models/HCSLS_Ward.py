from config import database, helpers, db_context
import datetime
import base
import threading
helpers.extent_model(
            "HCSLS_Ward",
            "base",
            [["ward_code"], ['district_code']],
            ward_code = ("text", True),
            district_code = ("text", True),
            ward_name = ("text", True),
            ward_name2 = ("text"),
            type_code = ("text"),
            ordinal=("numeric"),
            note=("text"),
            lock=("bool"),
            org_ward_code=("text"),
            created_on=("date"),
            created_by=("text"),
            modified_on=("date"),
            modified_by=("text")
        )
def HCSLS_Ward():
    ret = db_context.collection("HCSLS_Ward")
    return ret