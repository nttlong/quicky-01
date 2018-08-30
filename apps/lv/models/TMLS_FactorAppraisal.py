from config import database, helpers, db_context
import base
helpers.extent_model(
            "TMLS_FactorAppraisal",
            "base",
            [["factor_code"]],
            factor_code = ("text", True),
            factor_name = ("text", True),
            factor_name2 = ("text"),
            factor_group_code = ("text"),
            weight = ("numeric"),
            is_apply_all = ("bool"),
            job_working = ("list"),
            note = ("text"),
            ordinal = ("numeric"),
            lock = ("bool"),
            created_on=("date"),
            created_by=("text"),
            modified_on=("date"),
            modified_by=("text")
        )
def TMLS_FactorAppraisal():
    ret = db_context.collection("TMLS_FactorAppraisal")
    return ret