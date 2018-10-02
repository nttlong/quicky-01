from config import database, helpers, db_context
import base
helpers.extent_model(
            "TMLS_CompetencyGroup",
            "base",
            [["com_group_code"]],
            com_group_code=("text", True),
            com_group_name=("text", True),
            com_group_name2=("text"),
            parent_code=("text"),
            level=("numeric"),
            level_code=("list"),
            note=("text"),
            ordinal=("numeric"),
            lock=("bool")
        )

def TMLS_CompetencyGroup():
    ret = db_context.collection("TMLS_CompetencyGroup")
    return ret