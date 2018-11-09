from config import database, helpers, db_context
import base
import datetime
import uuid
helpers.extent_model(
            "TMPER_TargetKPI_Emp",
            "base",
            [["apr_period", "apr_year", "employee_code"]],
            rec_id=("text", True),
            apr_period=("numeric", True),
            apr_year=("numeric", True),
            employee_code=("text", True),
            join_date=("date"),
            job_w_code=("text"),
            is_modified=("bool"),
            assign_date=("date"),
            assigned_by=("text"),
            approver_code=("text"),
            approve_date=("date")
        )

def on_before_insert(data):
    data.update({
        "rec_id": str(uuid.uuid4())
        })

def on_before_update(data):
    pass
helpers.events("TMPER_TargetKPI_Emp").on_before_insert(on_before_insert).on_before_update(on_before_update)

def TMPER_TargetKPI_Emp():
    return db_context.collection("TMPER_TargetKPI_Emp")

