from config import database, helpers, db_context
import base
helpers.extent_model(
            "HCSLS_TrainSupplier",
            "base",
            [["tr_supplier_code"]],
            tr_supplier_code=("text", True),
            tr_supplier_name=("text", True),
            tr_supplier_name2=("text"),
            ordinal=("numeric"),
            note=("text"),
            lock=("bool"),
            created_on=("date"),
            created_by=("text"),
            modified_on=("date"),
            modified_by=("text")
            #department_code=("text")
        )
def HCSLS_TrainSupplier():
    ret = db_context.collection("HCSLS_TrainSupplier")
    return ret