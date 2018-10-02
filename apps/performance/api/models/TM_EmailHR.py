from config import database, helpers, db_context
import base
helpers.extent_model(
            "TM_EmailHR",
            "base",
            [["employee_code"]],
            employee_code=("text", True),
            email_address=("text"),
            department_code=("text"),
            note=("text")
        )

def TM_EmailHR():
    ret = db_context.collection("TM_EmailHR")
    return ret