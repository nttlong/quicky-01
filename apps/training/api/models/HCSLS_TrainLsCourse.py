from config import database, helpers, db_context
import base
helpers.extent_model(
            "HCSLS_TrainLsCourse",
            "base",
            [["course_code"]],
            course_code = ("text", True),
            course_name = ("text", True),
            course_name2 = ("text"),
            course_content = ("text"),
            train_group_code = ("text"),
            profession_code = ("text"),
            field_code = ("text"),
            method = ("text"),
            periodic = ("numeric"),
            number_month = ("numeric"),
            learner_min = ("numeric"),
            learner_max = ("numeric"),
            train_hours = ("text"),
            supplier_code = ("text"),
            room_code = ("text"),
            activity_task = ("text"),
            certificate_form = ("text"),
            after_month_work=("text"),
            note = ("text"),
            ordinal = ("numeric"),
            lock = ("bool"),
            created_on=("date"),
            created_by=("text"),
            modified_on=("date"),
            modified_by=("text")
        )
def HCSLS_TrainLsCourse():
    ret = db_context.collection("HCSLS_TrainLsCourse")
    return ret