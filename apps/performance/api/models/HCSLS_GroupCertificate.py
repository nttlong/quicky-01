from config import database, helpers, db_context
import base
helpers.extent_model(
            "HCSLS_GroupCertificate",
            "base",
            [["group_cer_code"]],
            group_cer_code=("text", True),
            group_cer_name=("text", True),
            group_cer_type=("numeric"),
            group_cer_by=("text"),
            group_cer_name2=("text"),
            ordinal=("numeric"),
            lock=("bool"),
            note=("text"),
            created_on=("date"),
            created_by=("text"),
            modified_on=("date"),
            modified_by=("text")
        )
def HCSLS_GroupCertificate():
    ret = db_context.collection("HCSLS_GroupCertificate")
    return ret