from config import database, helpers, db_context
import base
helpers.extent_model(
            "HCSLS_QuitJob",
            "base",
            [["quit_job_code"]],
            quit_job_code=("text", True),
            quit_job_name=("text", True),
            quit_type=("numeric"),
            ordinal=("numeric"),
            note=("text"),
            lock=("bool"),
            quit_job_name2=("text"),
            created_on=("date"),
            created_by=("text"),
            modified_on=("date"),
            modified_by=("text")
        )
def HCSLS_QuitJob():
    ret = db_context.collection("HCSLS_QuitJob")
    return ret