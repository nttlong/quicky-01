from config import database, helpers, db_context
import datetime
import base
import threading
helpers.extent_model(
            "HCSLS_EmployeeType",
            "base",
            [["emp_type_code"]],
            emp_type_code=("text", True),
            emp_type_name=("text", True),
            emp_type_name2=("text"),
            rate_main_sal=("numeric"),
            rate_soft_sal=("numeric"),
            true_type=("numeric", True),
            # probation_time_by=("numeric"),
            # probation_time=("text"),
            # is_fix=("numeric"),
            # coeff=("text"),
            # begin_date_cal=("numeric"),
            ordinal=("numeric"),
            note=("text"),
            lock=("bool"),
            created_on=("date"),
            created_by=("text"),
            modified_on=("date"),
            modified_by=("text")
            #department_code=("text")
        )
def HCSLS_EmployeeType():
    ret = db_context.collection("HCSLS_EmployeeType")
    return ret