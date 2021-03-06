from config import database, helpers, db_context
import datetime
_hasCreated=False

from qmongo import qview
from quicky import tenancy
import qmongo
def LMS_VW_Employee():
    return qview.create_mongodb_view(
            qmongo.models.HCSEM_Employees.aggregate.project(
            employee_code =  1,
            first_name =  1,
            last_name =  1,
            is_cbcc =  1,
            user_id = 1,
            full_name =  "concat(last_name, ' ', first_name)"
            )
            #.match('is_cbcc == {0}', True)
        ,
        "LMS_VW_Employee"
        )

helpers.extent_model(
            "HCSEM_Employees",
            "base",
            [["employee_code"]],
            photo_id=("text"),
            employee_code=("text", True),
            last_name=("text", True),
            first_name=("text", True),
            extra_name=("text"),
            gender=("numeric"),
            birthday=("date"),
            b_province_code=("text"),
            nation_code=("text"),
            ethnic_code=("text"),
            religion_code=("text"),
            culture_id=("numeric"),
            is_retrain=("numeric"),
            train_level_code=("text"),
            marital_code=("text"),
            id_card_no=("text"),
            issued_date=("date"),
            issued_place_code=("text"),
            mobile=("text"),
            p_phone=("text"),
            email=("text"),
            personal_email=("text"),
            document_no=("text"),
            join_date=("date", True),
            official_date=("date"),
            career_date=("date"),
            personnel_date=("date"),
            emp_type_code=("text"),
            labour_type=("numeric"),
            department_code=("text", True),
            job_pos_code=("text"),
            job_pos_date=("date"),
            job_w_code=("text", True),
            job_w_date=("date"),
            profession_code=("text"),
            level_management=("numeric"),
            is_cbcc=("bool"),
            is_expert_recruit=("bool"),
            is_expert_train=("bool"),
            manager_code=("text"),
            manager_sub_code=("text"),
            user_id=("text"),
            job_pos_hold_code=("text"),
            job_w_hold_code=("text"),
            department_code_hold=("text"),
            job_pos_hold_from_date=("date"),
            job_pos_hold_to_date=("date"),
            end_date=("date"),
            retire_ref_no=("text"),
            signed_date=("date"),
            signed_person=("text"),
            active=("bool"),
            note=("text"),
            p_address=("text"),
            p_province_code=("text"),
            p_district_code=("text"),
            p_ward_code=("text"),
            p_hamlet_code=("text"),
            t_address=("text"),
            t_province_code=("text"),
            t_district_code=("text"),
            t_ward_code=("text"),
            t_hamlet_code=("text"),
            foreigner=("bool"),
            vn_foreigner=("bool"),
            is_not_reside=("bool"),
            fo_working=("numeric"),
            fo_permiss=("text"),
            fo_begin_date=("date"),
            fo_end_date=("date"),
            created_on=("date"),
            created_by=("text"),
            modified_on=("date"),
            modified_by=("text")
        )

def HCSEM_Employees():
    global _hasCreated
    if not _hasCreated:
        dict_permission = dict()

        _hasCreated=True
    ret = db_context.collection("HCSEM_Employees")

    return ret