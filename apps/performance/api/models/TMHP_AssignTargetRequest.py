from config import database, helpers, db_context
import base
import datetime
helpers.extent_model(
            "TMHP_AssignTargetRequest",
            "base",
            [[]],
            request_status=("numeric"),
			is_modified=("bool"),
            created_on=("date"),
            created_by=("text"),
            modified_on=("date"),
            modified_by=("text")
        )
def TMHP_AssignTargetRequest():
    return db_context.collection("TMHP_AssignTargetRequest")

