from config import database, helpers, db_context
import datetime
_hasCreated=False

from qmongo import qview
from quicky import tenancy

def LMS_VW_Employee():
    return qview.create_mongodb_view(
            HCSEM_Employees().aggregate().project(
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

def HCSEM_Employees():
    global _hasCreated
    if not _hasCreated:
        dict_permission = dict()
        helpers.extent_model(
            "HCSEM_Employees",
            "base",
            [["employee_code"]],
            photo_id=helpers.create_field("text"),
            employee_code=helpers.create_field("text", True),
            last_name=helpers.create_field("text", True),
            first_name=helpers.create_field("text", True),
            extra_name=helpers.create_field("text"),
            gender=helpers.create_field("numeric"),
            birthday=helpers.create_field("date"),
            b_province_code=helpers.create_field("text"),
            nation_code=helpers.create_field("text"),
            ethnic_code=helpers.create_field("text"),
            religion_code=helpers.create_field("text"),
            culture_id=helpers.create_field("numeric"),
            is_retrain=helpers.create_field("numeric"),
            train_level_code=helpers.create_field("text"),
            marital_code=helpers.create_field("text"),
            id_card_no=helpers.create_field("text"),
            issued_date=helpers.create_field("date"),
            issued_place_code=helpers.create_field("text"),
            mobile=helpers.create_field("text"),
            p_phone=helpers.create_field("text"),
            email=helpers.create_field("text"),
            personal_email=helpers.create_field("text"),
            document_no=helpers.create_field("text"),
            join_date=helpers.create_field("date", True),
            official_date=helpers.create_field("date"),
            career_date=helpers.create_field("date"),
            personnel_date=helpers.create_field("date"),
            emp_type_code=helpers.create_field("text"),
            labour_type=helpers.create_field("numeric"),
            department_code=helpers.create_field("text", True),
            job_pos_code=helpers.create_field("text"),
            job_pos_date=helpers.create_field("date"),
            job_w_code=helpers.create_field("text", True),
            job_w_date=helpers.create_field("date"),
            profession_code=helpers.create_field("text"),
            level_management=helpers.create_field("numeric"),
            is_cbcc=helpers.create_field("bool"),
            is_expert_recruit=helpers.create_field("bool"),
            is_expert_train=helpers.create_field("bool"),
            manager_code=helpers.create_field("text"),
            manager_sub_code=helpers.create_field("text"),
            user_id=helpers.create_field("text"),
            job_pos_hold_code=helpers.create_field("text"),
            job_w_hold_code=helpers.create_field("text"),
            department_code_hold=helpers.create_field("text"),
            job_pos_hold_from_date=helpers.create_field("date"),
            job_pos_hold_to_date=helpers.create_field("date"),
            end_date=helpers.create_field("date"),
            retire_ref_no=helpers.create_field("text"),
            signed_date=helpers.create_field("date"),
            signed_person=helpers.create_field("text"),
            active=helpers.create_field("bool"),
            note=helpers.create_field("text"),
            p_address=helpers.create_field("text"),
            p_province_code=helpers.create_field("text"),
            p_district_code=helpers.create_field("text"),
            p_ward_code=helpers.create_field("text"),
            p_hamlet_code=helpers.create_field("text"),
            t_address=helpers.create_field("text"),
            t_province_code=helpers.create_field("text"),
            t_district_code=helpers.create_field("text"),
            t_ward_code=helpers.create_field("text"),
            t_hamlet_code=helpers.create_field("text"),
            foreigner=helpers.create_field("bool"),
            vn_foreigner=helpers.create_field("bool"),
            is_not_reside=helpers.create_field("bool"),
            fo_working=helpers.create_field("numeric"),
            fo_permiss=helpers.create_field("text"),
            fo_begin_date=helpers.create_field("date"),
            fo_end_date=helpers.create_field("date"),
            created_on=helpers.create_field("date"),
            created_by=helpers.create_field("text"),
            modified_on=helpers.create_field("date"),
            modified_by=helpers.create_field("text")
        )

        _hasCreated=True
    ret = db_context.collection("HCSEM_Employees")

    return ret