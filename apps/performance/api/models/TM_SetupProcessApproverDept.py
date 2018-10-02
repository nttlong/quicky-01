from config import database, helpers, db_context
from ...api import common
import base

helpers.extent_model(
            "TM_SetupProcessApproverDept",
            "base",
            [['process_id', 'approve_level', 'department_code']],
            process_id=helpers.create_field("text", True),
            approve_level=helpers.create_field("text", True),
            department_code=helpers.create_field("text", True),
            appover_code=helpers.create_field("list")
        )
def TM_SetupProcessApproverDept():
    ret = db_context.collection("TM_SetupProcessApproverDept")
    return ret