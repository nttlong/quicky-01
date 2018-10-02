from config import database, helpers, db_context
import datetime
import base
import threading
helpers.extent_model(
            "HCSLS_Hamlet",
            "base",
            [["hamlet_code"], ['ward_code']],
            hamlet_code = ("text", True),
            ward_code = ("text", True),
            hamlet_name = ("text", True),
            hamlet_name2 = ("text"),
            type_code = ("text"),
            ordinal=("numeric"),
            note=("text"),
            lock=("bool"),
            org_hamlet_code=("text"),
            created_on=("date"),
            created_by=("text"),
            modified_on=("date"),
            modified_by=("text")
        )
def HCSLS_Hamlet():
    ret = db_context.collection("HCSLS_Hamlet")
    return ret