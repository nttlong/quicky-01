from config import database, helpers, db_context
import datetime
import base
import threading
helpers.extent_model(
            "HCSLS_District",
            "base",
            [["district_code"], ['province_code']],
            district_code = ("text", True),
            province_code = ("text", True),
            district_name = ("text", True),
            district_name2 = ("text"),
            type_code = ("text"),
            ordinal=("numeric"),
            note=("text"),
            lock=("bool"),
            org_district_code=("text"),
            created_on=("date"),
            created_by=("text"),
            modified_on=("date"),
            modified_by=("text")
        )
def HCSLS_District():
    ret = db_context.collection("HCSLS_District")
    return ret