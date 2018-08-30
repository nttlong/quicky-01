from config import database, helpers, db_context

helpers.extent_model(
            "HCSLS_TrainCVRG",
            "base",
            [["train_cvrg_code"]],
            train_cvrg_code=("text", True),
            train_cvrg_name=("text", True),
            train_cvrg_name2=("text"),
            #is_lang=("bool"),
            #is_bhld=("bool"),
            ordinal=("numeric"),
            note=("text"),
            domain_code=("text", True),
            lock=("bool"),
            created_on=("date"),
            created_by=("text"),
            modified_on=("date"),
            modified_by=("text")
        )
def HCSLS_TrainCVRG():
    ret = db_context.collection("HCSLS_TrainCVRG")
    return ret