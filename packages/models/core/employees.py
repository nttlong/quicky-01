import pymqr
import datetime
@pymqr.documents.EmbededDocument()
class EmpExperience(object):
    """

    """
    def __init__(self):
        """

        """
        self.BeginDate = (datetime.datetime, True)
        self.EndDate = datetime.datetime
        self.Salary = int
        self.Currency_code =str
        self.EmpTypeCode = str
        self.JobPosCode = str
        self.JobWCode = str
        self.WorkingOn = str
        self.WorkingLocation = str
        self.Address =str
        self.ProfessionCode =str
        self.QuitJobCode = str
        self.Reason = str
        self.RefInfo = str
        self.Note = str
        self.IsNaCompany = str
        self.IsInSection = str

@pymqr.documents.Collection("employees")
class Emps(object):
    """
    Employee 
    """
    def __init__(self):
        self.PhotoId = ("text")
        self.Code = ("text", True)
        self.LastName = ("text", True)
        self.FirstName = ("text", True)
        self.Title = ("text")
        self.Gender = ("numeric")
        self.BirthDate = ("date")
        self.b_province_code = ("text")
        self.nation_code = ("text")
        self.ethnic_code = ("text")
        self.religion_code = ("text")
        self.culture_id = ("numeric")
        self.is_retrain = ("numeric")
        self.train_level_code = ("text")
        self.marital_code = ("text")
        self.id_card_no = ("text")
        self.issued_date = ("date")
        self.issued_place_code = ("text")
        self.mobile = ("text")
        self.p_phone = ("text")
        self.email = ("text")
        self.personal_email = ("text")
        self.document_no = ("text")
        self.join_date = ("date", True)
        self.official_date = ("date")
        self.career_date = ("date")
        self.personnel_date = ("date")
        self.emp_type_code = ("text")
        self.labour_type = ("numeric")
        self.department_code = ("text", True)
        self.job_pos_code = ("text")
        self.job_pos_date = ("date")
        self.job_w_code = ("text", True)
        self.job_w_date = ("date")
        self.profession_code = ("text")
        self.level_management = ("numeric")
        self.is_cbcc = ("bool")
        self.is_expert_recruit = ("bool")
        self.is_expert_train = ("bool")
        self.manager_code = ("text")
        self.manager_sub_code = ("text")
        self.user_id = ("text")
        self.job_pos_hold_code = ("text")
        self.job_w_hold_code = ("text")
        self.department_code_hold = ("text")
        self.job_pos_hold_from_date = ("date")
        self.job_pos_hold_to_date = ("date")
        self.end_date = ("date")
        self.retire_ref_no = ("text")
        self.signed_date = ("date")
        self.signed_person = ("text")
        self.active = ("bool")
        self.note = ("text")
        self.p_address = ("text")
        self.p_province_code = ("text")
        self.p_district_code = ("text")
        self.p_ward_code = ("text")
        self.p_hamlet_code = ("text")
        self.t_address = ("text")
        self.t_province_code = ("text")
        self.t_district_code = ("text")
        self.t_ward_code = ("text")
        self.t_hamlet_code = ("text")
        self.foreigner = ("bool")
        self.vn_foreigner = ("bool")
        self.is_not_reside = ("bool")
        self.fo_working = ("numeric")
        self.fo_permiss = ("text")
        self.fo_begin_date = ("date")
        self.fo_end_date = ("date")
        self.created_on = ("date")
        self.created_by = ("text")
        self.modified_on = ("date")
        self.modified_by = ("text")