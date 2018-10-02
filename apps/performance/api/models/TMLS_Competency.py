from config import database, helpers, db_context
import base
helpers.extent_model(
            "TMLS_Competency",
            "base",
            [["com_code"]],
            com_code=("text", True),
            com_name=("text", True),
            com_name2=("text"),
            com_group_code=("text"),
            com_type=("numeric", True),
            apr_form_type=("numeric", True),
            point_scale_type=("numeric", True),
            score_from=("numeric"),
            score_to=("numeric"),
            bu_codes=("text"),
            com_desc=("text"),
            note=("text"),
            ordinal=("numeric"),
            lock=("bool")
        )

def TMLS_Competency():
    ret = db_context.collection("TMLS_Competency")
    return ret