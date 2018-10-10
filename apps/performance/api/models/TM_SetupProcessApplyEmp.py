from config import database, helpers, db_context
from ...api import common
import base

helpers.extent_model(
            "TM_SetupProcessApplyEmp",
            "base",
            [['process_id', 'employee_code']],
            process_id=helpers.create_field("text", True),
            employee_code=helpers.create_field("text", True)
        )
def TM_SetupProcessApplyEmp():
    ret = db_context.collection("TM_SetupProcessApplyEmp")
    return ret