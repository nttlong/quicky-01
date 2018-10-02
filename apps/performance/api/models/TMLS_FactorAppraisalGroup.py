from config import database, helpers, db_context
import base
helpers.extent_model(
            "TMLS_FactorAppraisalGroup",
            "base",
            [["factor_group_code"]],
            factor_group_code = ("text", True),
            factor_group_name = ("text", True),
            factor_group_name2 = ("text"),
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
def TMLS_FactorAppraisalGroup():
    ret = db_context.collection("TMLS_FactorAppraisalGroup")
    return ret