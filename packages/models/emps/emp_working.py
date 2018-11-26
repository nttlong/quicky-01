import pymqr

import datetime
@pymqr.documents.EmbededDocument()
class EmpWorking(object):
    """
    The information of an Employee's Working 
    """
    def __init__(self):
        self.rec_id = (str, True)
        self.employee_code = (str, True)
        self.appoint = (int, True)
        self.effect_date = (datetime.datetime, True)
        self.begin_date = (datetime.datetime, True)
        self.end_date = (datetime.datetime)
        self.decision_no = (str, True)
        self.signed_date = (datetime.datetime)
        self.signer_code = (str)
        self.note = (str)
        self.task = (str)
        self.reason = (str)
        self.department_code = (str)
        self.job_pos_code = (str)
        self.job_w_code = (str)
        self.emp_type_code = (str)
        self.region_code = (str)
        self.department_code_old = (str)
        self.job_pos_code_old = (str)
        self.job_w_code_old = (str)
        self.emp_type_code_old = (str)
        self.region_code_old = (str)
        self.province_code = (str)
      
    
