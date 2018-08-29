from config import database, helpers, db_context
import base
helpers.extent_model(
            "HCSLS_Certificate",
            "base",
            [["cer_code"]],
            cer_code=("text", True),
            cer_name=("text", True),
            cer_name2=("text"),
            expired_time=("numeric"),
            group_cer_code=("text"),
            cers_time_limit=("numeric"),
            scer_code=("text"),
            cers_replace_code=("text"),
            ordinal=("numeric"),
            note=("text"),
            lock=("bool"),
            created_on=("date"),
            created_by=("text"),
            modified_on=("date"),
            modified_by=("text")
        )
def HCSLS_Certificate():
    ret = db_context.collection("HCSLS_Certificate")
    return ret