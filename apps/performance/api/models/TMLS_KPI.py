from config import database, helpers, db_context
import base
helpers.extent_model(
            "TMLS_KPI",
            "base",
            [["kpi_code"]],
            kpi_code = ("text", True),
            kpi_name = ("text", True),
            kpi_name2 = ("text"),
            kpi_group_code = ("text"),
            unit_code=("text"),
            cycle_type=("numeric"),
            kpi_desc=("text"),
            kpi_ref=("text"),
            weight=("numeric"),
            benchmark=("numeric"),
            kpi_formula=("text"),
            value_cal_type=("numeric", True),
            input_type=("numeric"),
            is_apply_all=("bool"),
            kpi_years=("text"),
            score_from=("numeric"),
            score_to=("numeric"),
            note=("text"),
            lock=("bool"),
            created_on=("date"),
            created_by=("text"),
            modified_on=("date"),
            modified_by=("text")
        )
def TMLS_KPI():
    ret = db_context.collection("TMLS_KPI")
    return ret