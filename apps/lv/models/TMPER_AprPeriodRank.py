from config import database, helpers, db_context
import base
helpers.extent_model(
            "TMPER_AprPeriodRank",
            "base",
            [["apr_period","apr_year","department_code"]],
            apr_period=("numeric", True),
            apr_year=("numeric", True),
            department_code=("text"),
            rank_code=("text"),
            percent=("numeric"),
            note=("text"),
            created_on=("date"),
            created_by=("text"),
            modified_on=("date"),
            modified_by=("text")
        )
def TMPER_AprPeriodRank():
    ret = db_context.collection("TMPER_AprPeriodRank")
    return ret