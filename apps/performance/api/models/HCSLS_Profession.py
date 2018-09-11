from config import database, helpers, db_context
import base
helpers.extent_model(
            "HCSLS_Profession",
            "base",
            [["profession_code"]],
            profession_code=("text", True),
            profession_name=("text", True),
            note=("text"),
            ordinal=("numeric"),
            lock=("bool"),
            profession_name2=("text"),
            created_on=("date"),
            created_by=("text"),
            modified_on=("date"),
            modified_by=("text")
        )
def HCSLS_Profession():
    ret = db_context.collection("HCSLS_Profession")
    return ret