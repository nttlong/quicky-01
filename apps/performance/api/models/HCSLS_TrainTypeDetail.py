from config import database, helpers, db_context
import base
helpers.extent_model(
            "HCSLS_TrainTypeDetail",
            "base",
            [["train_detail_code"]],
            train_detail_code=("text", True),
            train_detail_name=("text", True),
            train_detail_name2=("text"),
            ordinal=("numeric"),
            note=("text"),
            lock=("bool"),
            created_on=("date"),
            created_by=("text"),
            modified_on=("date"),
            modified_by=("text")
            #department_code=("text")
        )
def HCSLS_TrainTypeDetail():
    ret = db_context.collection("HCSLS_TrainTypeDetail")
    return ret