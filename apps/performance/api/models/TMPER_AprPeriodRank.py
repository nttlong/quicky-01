from config import database, helpers, db_context
import base
helpers.extent_model(
            "TMPER_AprPeriodRank",
            "base",
            [["apr_period","apr_year","department_code"]],
            apr_period=helpers.create_field("numeric", True),
            apr_year=helpers.create_field("numeric", True),
            department_code=helpers.create_field("text"),
            rank_level =helpers.create_field("list"),
            note=helpers.create_field("text"),
            created_on=helpers.create_field("date"),
            created_by=helpers.create_field("text"),
            modified_on=helpers.create_field("date"),
            modified_by=helpers.create_field("text")
        )
def TMPER_AprPeriodRank():
    ret = db_context.collection("TMPER_AprPeriodRank")

    return ret