from config import database, helpers, db_context
import base
helpers.extent_model(
            "HCSLS_TrainRequest",
            "base",
            [["request_code"]],
            request_code = ("text", True),
            course_name = ("text", True),
            reason_train = ("text"),
            year = ("numeric"),
            quarter = ("numeric"),
            month = ("numeric"),
            cost_estimate = ("text"),
            address = ("text"),
            department_request = ("text"),
            proponent = ("text"),
            note = ("text"),
            ordinal = ("numeric"),
            lock = ("bool"),
            created_on=("date"),
            created_by=("text"),
            modified_on=("date"),
            modified_by=("text")
        )
def HCSLS_TrainRequest():
    ret = db_context.collection("HCSLS_TrainRequest")
    return ret