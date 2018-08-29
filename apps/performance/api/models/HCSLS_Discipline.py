from config import database, helpers, db_context
import base
helpers.extent_model(
            "HCSLS_Discipline",
            "base",
            [["disc_code"]],
            disc_code=("text", True),
            disc_name=("text", True),
            is_due_salary=("bool"),
            ordinal=("numeric"),
            note=("text"),
            lock=("bool"),
            disc_name2=("text"),
            created_on=("text"),
            created_by=("date"),
            modified_on=("text"),
            modified_by=("date")
        )
def HCSLS_Discipline():
    ret = db_context.collection("HCSLS_Discipline")
    return ret