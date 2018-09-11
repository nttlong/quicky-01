from config import database, helpers, db_context
import base
helpers.extent_model(
            "HCSLS_Nation",
            "base",
            [["nation_code"]],
            nation_code=("text", True),
            nation_name=("text", True),
            ordinal=("numeric"),
            note=("text"),
            lock=("bool"),
            continents=("numeric"),
            #eat_amount=("numeric"),
            #home_amount=("numeric"),
            #taxi_amount=("numeric"),
            #sub_days_amount=("numeric"),
            nation_name2=("text"),
            created_on=("date"),
            created_by=("text"),
            modified_on=("date"),
            modified_by=("text"),
            #department_code=("text"),
            org_nation_code=("text")
        )
def HCSLS_Nation():
    ret = db_context.collection("HCSLS_Nation")
    return ret