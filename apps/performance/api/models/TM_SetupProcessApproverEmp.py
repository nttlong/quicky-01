from config import database, helpers, db_context
from ...api import common
import base

helpers.extent_model(
            "TM_SetupProcessApproverEmp",
            "base",
            [['process_id', 'approve_level', 'employee_code']],
            process_id=helpers.create_field("text", True),
            approve_level=helpers.create_field("text", True),
            employee_code=helpers.create_field("text", True),
            appover_code=helpers.create_field("list")
        )
def TM_SetupProcessApproverEmp():
    ret = db_context.collection("TM_SetupProcessApproverEmp")
    return ret