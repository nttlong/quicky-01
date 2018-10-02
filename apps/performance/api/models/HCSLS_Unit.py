from config import database, helpers, db_context
import base
helpers.extent_model(
            "HCSLS_Unit",
            "base",
            [["unit_code"]],
			unit_code=("text", True),
            unit_name=("text", True),
            unit_name2=("text"),
            note=("text"),
			lock=("bool"),
            ordinal=("numeric"),
            created_on=("date"),
            created_by=("text"),
            modified_on=("date"),
            modified_by=("text")
        )
def HCSLS_Unit():
    ret = db_context.collection("HCSLS_Unit")
    return ret


