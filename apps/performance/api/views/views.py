from qmongo import qview
from quicky import tenancy
from ..models.HCSEM_Employees import HCSEM_Employees
from ..models.HCSEM_Employees import HCSEM_Employees
from ..models.HCSSYS_Departments import HCSSYS_Departments
from ..models.HCSLS_Position import HCSLS_Position
from ..models.HCSLS_JobWorking import HCSLS_JobWorking
from ..models.HCSLS_Region import HCSLS_Region
from ..models.SYS_ValueList import SYS_ValueList
from ..models.TM_EmailHR import TM_EmailHR
from ..models.HCSEM_EmpWorking import HCSEM_EmpWorking
from ..models.TMPER_AprPeriod import TMPER_AprPeriod
import qmongo
def SYS_VW_ValueList():
    return qview.create_mongodb_view(
        SYS_ValueList().aggregate().unwind("values").project(
            language = "language",
            list_name = "list_name",
            multi_select = "multi_select",
            description = "description",
            created_on = "created_on",
            created_by = "created_by",
            modified_on = "modified_on",
            modified_by = "modified_by",
            value = "values.value",
            caption = "values.caption",
            custom = "values.custom"
            )
        ,
        "SYS_VW_ValueList"
        )

def HCSEM_VW_EmployeeCBCC():
    return qview.create_mongodb_view(
            qmongo.models.HCSEM_Employees.aggregate.project(
            employee_code =  1,
            first_name =  1,
            last_name =  1,
            is_cbcc =  1,
            full_name =  "concat(last_name, ' ', first_name)"
            ).match('is_cbcc == {0}', True)
        ,
        "HCSEM_VW_EmployeeCBCC"
        )

# def HCSEM_VW_Employee_FullName_And_Email():
#     return qview.create_mongodb_view(
#             HCSEM_Employees().aggregate().project(
#             employee_code =  1,
#             first_name =  1,
#             last_name =  1,
#             email =  1,
#             full_name =  "concat(last_name, ' ', first_name)"
#             )
#         ,
#         "HCSEM_VW_Employee_FullName_And_Email"
#         )

# def HCSLS_VW_JobWorkingFactorAppraisal():
#     return qview.create_mongodb_view(
#             HCSLS_JobWorking().aggregate().unwind("factor_appraisal", False).project(
#                 rec_id = "factor_appraisal.rec_id",
#                 factor_code =  "factor_appraisal.factor_code",
#                 job_w_name = "job_w_name",
#                 job_w_code =  "factor_appraisal.job_w_code",
#                 weight = "factor_appraisal.weight",
#                 created_on= "factor_appraisal.created_on",
#                 created_by= "factor_appraisal.created_by",
#                 modified_on= "factor_appraisal.modified_on",
#                 modified_by= "factor_appraisal.modified_by"
#                 )
#         ,
#         "HCSLS_VW_JobWorkingFactorAppraisal"
#         )

# def HCSLS_VW_JobWorkingKPI():
#     return qview.create_mongodb_view(
#             HCSLS_JobWorking().aggregate().unwind("kpi", False).project(
#                 rec_id = "kpi.rec_id",
#                 kpi_code = "kpi.kpi_code",
#                 job_w_code = "job_w_code",
#                 job_w_name = "job_w_name",
#                 kpi_name = "kpi.kpi_name",
#                 unit = "kpi.unit",
#                 description = "kpi.description",
#                 cycle = "kpi.cycle",
#                 weight = "kpi.weight",
#                 standard_mark = "kpi.standard_mark",
#                 score_from = "kpi.score_from",
#                 score_to = "kpi.score_to",
#                 ordinal = "kpi.ordinal",
#                 note = "kpi.note",
#                 created_on = "kpi.created_on",
#                 created_by = "kpi.created_by",
#                 modified_on = "kpi.modified_on",
#                 modified_by = "kpi.modified_by"
#                 )
#         ,
#         "HCSLS_VW_JobWorkingKPI"
#         )

# def HCSLS_VW_JobWorkingCompetency():
#     return qview.create_mongodb_view(
#             HCSLS_JobWorking().aggregate().unwind("competency", False).project(
#                 rec_id = "competency.rec_id",
#                 job_w_code = "job_w_code",
#                 job_w_name = "job_w_name",
#                 grade = "competency.grade",
#                 com_code = "competency.com_code",
#                 com_level_code = "competency.com_level_code",
#                 weight = "competency.weight",
#                 ordinal = "competency.ordinal",
#                 note = "competency.note",
#                 created_on = "competency.created_on",
#                 created_by = "competency.created_by",
#                 modified_on = "competency.modified_on",
#                 modified_by = "competency.modified_by"
#                 )
#         ,
#         "HCSLS_VW_JobWorkingCompetency"
#         )

# def HCSEM_VWEmpWorking():
#     return qview.create_mongodb_view(
#
#             HCSEM_EmpWorking().aggregate()
#             .join(HCSSYS_Departments(), 'department_code', 'department_code', 'dept')
#             .join(HCSSYS_Departments(), 'department_code_old', 'department_code', 'dept_old')
#             .join(HCSLS_Position(), 'job_pos_code', 'job_pos_code', 'job_pos')
#             .join(HCSLS_Position(), 'job_pos_code_old', 'job_pos_code', 'job_pos_old')
#             .join(HCSLS_JobWorking(), 'job_w_code', 'job_w_code', 'job_w')
#             .join(HCSLS_JobWorking(), 'job_w_code_old', 'job_w_code', 'job_w_old')
#             .join(HCSLS_Region(), 'region_code', 'region_code', 'region')
#             .join(HCSLS_Region(), 'region_code_old', 'region_code', 'region_old')
#
#             #.join(SYS_ValueList().aggregate().match("list_name == {0}", "HCS.LoaiQuyetDinhBoNhiem_DieuChuyen").unwind("values"), "appoint", "value", "values_list")
#             .project(
#             employee_code =  1,
#             appoint =  1,
#            # appoint_name = "values_list.caption",
#             effect_date = 1,
#             begin_date = 1,
#             end_date = 1,
#             decision_no = 1,
#             signed_date = 1,
#             signer_code = 1,
#             note =1,
#             task = 1,
#             reason =1,
#             department_code = 1,
#             job_pos_code = 1,
#             job_w_code = 1,
#             emp_type_code = 1,
#             region_code = 1,
#             department_code_old = 1,
#             job_pos_code_old = 1,
#             job_w_code_old = 1,
#             emp_type_code_old = 1,
#             region_code_old = 1,
#             province_code = 1,
#             department_name = "dept.department_name",
#             job_pos_name = "job_pos.job_pos_name",
#             job_w_name = "job_w.job_w_name",
#             region_name = "region.region_name",
#             department_name_old = "dept_old.department_name",
#             job_pos_name_old = "job_pos_old.job_pos_name",
#             job_w_name_old = "job_w_old.job_w_name",
#             region_name_old = "region_old.region_name",
#             created_by = 1,
#             created_on = 1,
#             modified_on = 1,
#             modified_by = 1
#             )
#             #.match('is_cbcc == {0}', True)
#         ,
#         "HCSEM_VWEmpWorking"
#         )

# def TM_VW_EmailHR():
#     return qview.create_mongodb_view(
#         TM_EmailHR().aggregate()
#             .lookup(HCSEM_Employees(), "employee_code", "employee_code", "emp")
#             .unwind("emp", False)
#             .lookup(HCSSYS_Departments(), "department_code", "department_code", "dept")
#             .unwind("dept", False)
#             .project(
#             employee_code = "employee_code",
#             email_address="email_address",
#             department_code="department_code",
#             note="note",
#             department_name="switch(case(dept.department_name!='',dept.department_name),'')",
#             employee_name="concat(emp.last_name, ' ', emp.first_name)"
#         )
#         ,
#         "TM_VW_EmailHR"
#     )

# def TMPER_VW_AprPeriod():
#     return qview.create_mongodb_view(
#         TMPER_AprPeriod().aggregate().lookup(SYS_VW_ValueList(), "apr_period", "value", "val")\
#         .unwind("val", False)\
#         .match("expr(strcasecmp(val.list_name, 'LApprovalPeriod') == 0)")\
#         .project(
#             apr_period=1,
#             apr_year=1,
#             give_target_from=1,
#             give_target_to=1,
#             review_mid_from=1,
#             review_mid_to=1,
#             approval_mid_from=1,
#             approval_mid_to=1,
#             emp_final_from=1,
#             emp_final_to=1,
#             approval_final_from=1,
#             approval_final_to=1,
#             note=1,
#             apr_period_name = "val.caption",
#             apr_name="concat(val.caption, '/', substr(apr_year,0,-1))",
#             apr_code="concat(substr(apr_period,0,-1), '-', substr(apr_year,0,-1))"
#         ),
#         "TMPER_VW_AprPeriod"
#     )