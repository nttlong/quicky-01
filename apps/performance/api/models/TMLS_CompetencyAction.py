from config import database, helpers, db_context
import base
helpers.extent_model(
            "TMLS_CompetencyAction",
            "base",
            [["com_code", "com_level_code", "action"]],
            com_code=("text", True),
            com_level_code=("text", True),
            action=("text", True),
            weight=("numeric"),
            ordinal=("numeric")
        )

def TMLS_CompetencyAction():
    ret = db_context.collection("TMLS_CompetencyAction")
    return ret