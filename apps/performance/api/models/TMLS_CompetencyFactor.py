from config import database, helpers, db_context
import base
helpers.extent_model(
            "TMLS_CompetencyFactor",
            "base",
            [["com_code", "factor"]],
            com_code=("text", True),
            factor=("text", True),
            weight=("numeric"),
            com_level_code=("text"),
            ordinal=("numeric")
        )

def TMLS_CompetencyFactor():
    ret = db_context.collection("TMLS_CompetencyFactor")
    return ret