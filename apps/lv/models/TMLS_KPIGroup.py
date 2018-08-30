from config import database, helpers, db_context
import base
helpers.extent_model(
            "TMLS_KPIGroup",
            "base",
            [["kpi_group_code"]],
            kpi_group_code = ("text", True),
            kpi_group_name = ("text", True),
            kpi_group_name2 = ("text"),
            parent_code = ("text"),
            level = ("numeric"),
            level_code = ("list"),
            weight = ("numeric"),
            is_team = ("bool"),
            note = ("text"),
            ordinal = ("numeric"),
            lock = ("bool"),
            created_by=("text"),
            modified_on=("date"),
            modified_by=("text")
        )
def TMLS_KPIGroup():
    ret = db_context.collection("TMLS_KPIGroup")
    return ret