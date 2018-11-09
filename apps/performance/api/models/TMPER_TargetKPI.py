from config import database, helpers, db_context
import base
import uuid
helpers.extent_model(
            "TMPER_TargetKPI",
            "base",
            [["apr_period", "apr_year", "employee_code", "target_name"]],
            rec_id=("text", True),
            ref_id=("text", True),
            apr_period=("numeric", True),
            apr_year=("numeric", True),
            employee_code=("text", True),
            target_name=("text", True),
            kpi_code=("text"),
            unit_code=("text"),
            cycle_type=("numeric"),
            target_desc=("text"),
            weight=("numeric"),
            kpi_formula=("text"),
            value_cal_type=("numeric"),
            parent_name=("text"),
            parent_code=("text"),
            bsc_type=("numeric"),
            begin_date=("date"),
            end_date=("date"),
            baseline=("text"),
            min_value=("text"),
            max_value=("text"),
            target=("text"),
            origin_target=("text"),
            perform=("text"),
            note=("text"),
            complete_pct=("numeric"),
            complete_date=("date"),
            modify_type=("numeric")
        )

def on_before_insert(data):
    data.update({
        "rec_id": str(uuid.uuid4())
        })

def on_before_update(data):
    pass
helpers.events("TMPER_TargetKPI").on_before_insert(on_before_insert).on_before_update(on_before_update)

def TMPER_TargetKPI():
    return db_context.collection("TMPER_TargetKPI")

