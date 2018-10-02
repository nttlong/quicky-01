from config import database, helpers, db_context
import base
helpers.extent_model(
            "HCSLS_Region",
            "base",
            [["region_code"]],
            region_code=("text", True),
            region_name=("text", True),
            region_name2=("text"),
            ordinal=("numeric"),
            note=("text"),
            lock=("bool"),
            created_on=("date"),
            created_by=("text"),
            modified_on=("date"),
            modified_by=("text")
            #department_code=("text")
        )
def HCSLS_Region():
    ret = db_context.collection("HCSLS_Region")
    return ret