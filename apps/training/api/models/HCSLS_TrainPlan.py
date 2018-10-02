from config import database, helpers, db_context
import base
helpers.extent_model(
            "HCSLS_TrainPlan",
            "base",
            [["course_code"]],
            course_code = ("text", True),
            course_name = ("text", True),
            from_day = ("date"),
            to_day = ("date"),
            year = ("numeric"),
            quarter = ("numeric"),
            wave = ("numeric"),
            check = ("bool"),
            scheduler = ("bool"),
            number = ("numeric"),
            method = ("text"),
            address = ("text"),
            room = ("text"),
            teacher = ("text"),
            note = ("text"),
            ordinal = ("numeric"),
            lock = ("bool"),
            created_on=("date"),
            created_by=("text"),
            modified_on=("date"),
            modified_by=("text")
        )
def HCSLS_TrainPlan():
    ret = db_context.collection("HCSLS_TrainPlan")
    return ret