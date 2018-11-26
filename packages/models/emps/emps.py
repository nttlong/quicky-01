import pymqr
import datetime


@pymqr.documents.Collection("employees")
class Emps(object):
    """
    Employee 
    """
    def __init__(self):
        self.PhotoId = str
        self.Code = (str, True)
        self.LastName = (str, True)
        self.FirstName = (str, True)
        self.Title = str
        self.Gender = int
        self.BirthDate = datetime.datetime
        self.b_province_code = str
        self.nation_code = str
        self.ethnic_code = str
        self.religion_code = str
        self.culture_id = int
        self.is_retrain = int
        self.train_level_code = str
        self.marital_code = str
        self.id_card_no = str
        self.issued_date = datetime.datetime
        self.issued_place_code = str
        self.mobile = str
        self.p_phone = str
        self.email = str
        self.personal_email = str
        self.document_no = str
        self.join_date = ( datetime.datetime, True)
        self.official_date = datetime.datetime
        self.career_date = datetime.datetime
        self.personnel_date = datetime.datetime
        self.emp_type_code = str
        self.labour_type = int
        self.department_code = (str, True)
        self.job_pos_code = str
        self.job_pos_date = datetime.datetime
        self.job_w_code = (str, True)
        self.job_w_date = datetime.datetime
        self.profession_code = str
        self.level_management = int
        self.is_cbcc = bool
        self.is_expert_recruit = bool
        self.is_expert_train = bool
        self.manager_code = str
        self.manager_sub_code = str
        self.user_id = str
        self.job_pos_hold_code = str
        self.job_w_hold_code = str
        self.department_code_hold = str
        self.job_pos_hold_from_date = datetime.datetime
        self.job_pos_hold_to_date = datetime.datetime
        self.end_date = datetime.datetime
        self.retire_ref_no = str
        self.signed_date = datetime.datetime
        self.signed_person = str
        self.active = bool
        self.note = str
        self.p_address = str
        self.p_province_code = str
        self.p_district_code = str
        self.p_ward_code = str
        self.p_hamlet_code = str
        self.t_address = str
        self.t_province_code = str
        self.t_district_code = str
        self.t_ward_code = str
        self.t_hamlet_code = str
        self.foreigner = bool
        self.vn_foreigner = bool
        self.is_not_reside = bool
        self.fo_working = int
        self.fo_permiss = str
        self.fo_begin_date = datetime.datetime
        self.fo_end_date = datetime.datetime
        self.created_on = datetime.datetime
        self.created_by = str
        self.modified_on = datetime.datetime
        self.modified_by = str