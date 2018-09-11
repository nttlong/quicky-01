from config import database, helpers, db_context
import base
helpers.extent_model(
            "HCSLS_TrainDomain",
            "base",
            [["domain_code"]],
            domain_code=("text", True),
            domain_name=("text", True),
            ordinal=("numeric"),
            note=("text"),
            lock=("bool"),
            domain_name2=("text"),
            created_on=("date"),
            created_by=("text"),
            modified_on=("date"),
            modified_by=("text")
        )
def HCSLS_TrainDomain():
    ret = db_context.collection("HCSLS_TrainDomain")
    return ret