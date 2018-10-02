from config import database, helpers, db_context
import base
helpers.extent_model(
            "TMPER_AprPeriodEmpOut",
            "base",
            [['apr_period', 'apr_year', 'employee_code']],
            apr_period=("numeric", True),
            apr_year=("numeric", True),
            employee_code=("text"),
            department_code=("text"),
            job_w_code=("text"),
            reason=("text"),
            note=("text"),
            created_on=("date"),
            created_by=("text"),
            modified_on=("date"),
            modified_by=("text")
        )
def TMPER_AprPeriodEmpOut():
    ret = db_context.collection("TMPER_AprPeriodEmpOut")
    return ret