from config import database, helpers, db_context
from ...api import common

import datetime
_hasCreated=False
helpers.extent_model(
            "HCSEM_EmpExperience",
            "base",
            [['rec_id']],
            rec_id =("text", True),
            employee_code=("text"),
            begin_date=("date", True),
            end_date=("date"),
            salary=("numeric", True),
            currency_code=("text"),
            emp_type_code=("text"),
            job_pos_code=("text"),
            job_w_code=("text"),
            working_on=("text"),
            working_location=("text", True),
            address=("text"),
            profession_code=("text"),
            quit_job_code=("text"),
            reason=("text"),
            ref_info=("text"),
            note=("text"),
            is_na_company=("bool"),
            is_in_section=("bool"),
            created_on=("date"),
            created_by=("text"),
            modified_on=("date"),
            modified_by=("text")
        )
def on_before_insert(data):
    data.update({
        "rec_id": common.generate_guid()
        })

def on_before_update(data):
    pass

helpers.events("HCSEM_EmpExperience").on_before_insert(on_before_insert).on_before_update(on_before_update)
def HCSEM_EmpExperience():
    ret = db_context.collection("HCSEM_EmpExperience")
    return ret