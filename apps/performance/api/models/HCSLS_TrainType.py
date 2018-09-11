from config import database, helpers, db_context
import base
helpers.extent_model(
            "HCSLS_TrainType",
            "base",
            [["train_mode_code"]],
            train_mode_code=("text", True),
            train_mode_name=("text", True),
            train_mode_name2=("text"),
            ordinal=("numeric"),
            note=("text"),
            lock=("bool"),
            created_on=("date"),
            created_by=("text"),
            modified_on=("date"),
            modified_by=("text")
            #department_code=("text")
        )
def HCSLS_TrainType():

    ret = db_context.collection("HCSLS_TrainType")

    return ret