from config import database, helpers, db_context
import base
helpers.extent_model(
            "HCSLS_Marital",
            "base",
            [["marital_code"]],
            marital_code=("text", True),
            marital_name=("text", True),
            ordinal=("numeric"),
            note=("text"),
            lock=("bool"),
            marital_name2=("text"),
            created_on=("text"),
            created_by=("date"),
            modified_on=("text"),
            modified_by=("date")
        )
def HCSLS_Marital():
    ret = db_context.collection("HCSLS_Marital")
    return ret