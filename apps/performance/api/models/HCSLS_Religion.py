from config import database, helpers, db_context
import base
helpers.extent_model(
            "HCSLS_Religion",
            "base",
            [["religion_code"]],
            religion_code=("text", True),
            religion_name=("text", True),
            ordinal=("numeric"),
            note=("text"),
            lock=("bool"),
            religion_name2=("text"),
            created_on=("text"),
            created_by=("date"),
            modified_on=("text"),
            modified_by=("date")
        )
def HCSLS_Religion():
    ret = db_context.collection("HCSLS_Religion")
    return ret