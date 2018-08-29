from config import database, helpers, db_context
import base
helpers.extent_model(
            "HCSLS_Ethnic",
            "base",
            [["ethnic_code"]],
            ethnic_code=("text", True),
            ethnic_name=("text", True),
            range=("numeric"),
            ordinal=("numeric"),
            note=("text"),
            lock=("bool"),
            ethnic_name2=("text"),
            is_ethnic_minority=("bool"),
            created_on=("text"),
            created_by=("date"),
            modified_on=("text"),
            modified_by=("date")
        )
def HCSLS_Ethnic():
    ret = db_context.collection("HCSLS_Ethnic")
    return ret