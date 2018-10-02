from config import database, helpers, db_context
import base
helpers.extent_model(
            "TMLS_CompetencyLevel",
            "base",
            [["com_code", "com_level_code"]],
            com_code=("text", True),
            com_level_code=("text", True),
            com_level_name=("text"),
            com_level_name2=("text"),
            score_from=("numeric"),
            score_to=("numeric"),
            note=("text"),
            ordinal=("numeric")
        )

def TMLS_CompetencyLevel():
    ret = db_context.collection("TMLS_CompetencyLevel")
    return ret