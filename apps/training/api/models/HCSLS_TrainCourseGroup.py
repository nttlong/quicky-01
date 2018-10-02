from config import database, helpers, db_context
import base
helpers.extent_model(
            "HCSLS_TrainCourseGroup",
            "base",
            [["train_group_code"]],
            train_group_code = ("text", True),
            train_group_name = ("text", True),
            train_group_name2 = ("text"),
            parent_code = ("text"),
            level = ("numeric"),
            level_code = ("list"),
            note = ("text"),
            ordinal = ("numeric"),
            lock = ("bool"),
            created_by=("text"),
            modified_on=("date"),
            modified_by=("text")
        )
def HCSLS_TrainCourseGroup():
    ret = db_context.collection("HCSLS_TrainCourseGroup")
    return ret