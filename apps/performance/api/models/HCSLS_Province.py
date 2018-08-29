from config import database, helpers, db_context
import datetime
import base
import threading
helpers.extent_model(
            "HCSLS_Province",
            "base",
            [["province_code"]],
            province_code=("text",True),
            province_name=("text", True),
            province_name2=("text"),
            type_code=("text"),
            region_code=("text"),
            nation_code=("text"),
            ordinal=("numeric"),
            note=("text"),
            lock=("bool"),
            org_province_code=("text"),
            created_on=("date"),
            created_by=("text"),
            modified_on=("date"),
            modified_by=("text")
        )
def HCSLS_Province():
    ret = db_context.collection("HCSLS_Province")
    return ret