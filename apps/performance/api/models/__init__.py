import quicky
from qmongo import database
app=quicky.applications.get_app_by_file(__file__)
db_context=database.connect(app.settings.Database)
from SYS_FunctionList import SYS_FunctionList
from HCSSYS_DataDomain import HCSSYS_DataDomain
from HCSSYS_Departments import HCSSYS_Departments
from SYS_ValueList import SYS_ValueList
from HCSSYS_SystemConfig import HCSSYS_SystemConfig
from auth_user import auth_user
from auth_user_info import auth_user_info
from AD_Roles import AD_Roles
from HCSSYS_ComboboxList import HCSSYS_ComboboxList
from HCSLANG_CollectionInfo import HCSLANG_CollectionInfo
from HCSSYS_CollectionInfo import HCSSYS_CollectionInfo
from HCSSYS_ExcelTemplate import HCSSYS_ExcelTemplate
from HCSLS_EmployeeType import HCSLS_EmployeeType
from HCSLS_Nation import HCSLS_Nation
from HCSLS_Region import HCSLS_Region
from HCSLS_Ethnic import HCSLS_Ethnic
from HCSLS_Marital import HCSLS_Marital
from HCSLS_Religion import HCSLS_Religion
from HCSLS_QuitJob import HCSLS_QuitJob
from HCSLS_Certificate import HCSLS_Certificate
from HCSLS_GroupCertificate import HCSLS_GroupCertificate
from HCSLS_TrainTypeDetail import HCSLS_TrainTypeDetail
from HCSLS_TrainSupplier import HCSLS_TrainSupplier
from HCSLS_TrainCVRG import HCSLS_TrainCVRG
from HCSLS_TrainDomain import HCSLS_TrainDomain
from HCSLS_TrainType import HCSLS_TrainType
from HCSLS_Profession import HCSLS_Profession
from HCSLS_Acadame import HCSLS_Acadame
from HCSLS_Position import HCSLS_Position
from HCSLS_Award import HCSLS_Award
from HCSLS_AwardLevel import HCSLS_AwardLevel
from HCSLS_AwardPlace import HCSLS_AwardPlace
from HCSLS_Province import HCSLS_Province
from HCSLS_District import HCSLS_District
from HCSLS_Ward import HCSLS_Ward
from HCSLS_Hamlet import HCSLS_Hamlet
from HCSLS_Discipline import HCSLS_Discipline
from HCSEM_Employees import HCSEM_Employees
from HCSLS_JobWorkingGroup import HCSLS_JobWorkingGroup
from HCSLS_JobWorking import HCSLS_JobWorking
from TMLS_Rank import TMLS_Rank
from TMSYS_ConfigChangeObjectPriority import TMSYS_ConfigChangeObjectPriority
from TMLS_FactorAppraisal import TMLS_FactorAppraisal
from TMLS_FactorAppraisalGroup import TMLS_FactorAppraisalGroup
from TMLS_KPIGroup import TMLS_KPIGroup
from TMLS_KPI import TMLS_KPI
from tmp_transactions import tmp_transactions
from HCSEM_EmpWorking import HCSEM_EmpWorking
from HCSLS_Currency import HCSLS_Currency
from HCSLS_Unit import HCSLS_Unit
from HCSEM_EmpExperience import HCSEM_EmpExperience
from TMPER_AprPeriod import TMPER_AprPeriod
from TMPER_AprPeriodRank import TMPER_AprPeriodRank
from TMPER_AprPeriodEmpOut import TMPER_AprPeriodEmpOut
from HCSSYS_FunctionListSummary import HCSSYS_FunctionListSummary
from TMLS_Competency import TMLS_Competency
from TMLS_CompetencyAction import TMLS_CompetencyAction
from TMLS_CompetencyFactor import TMLS_CompetencyFactor
from TMLS_CompetencyGroup import TMLS_CompetencyGroup
from TMLS_CompetencyLevel import TMLS_CompetencyLevel
from TM_EmailTemplate import TM_EmailTemplate
from HCSSYS_AttachmentFile import HCSSYS_AttachmentFile
from TM_SetupProcessApproverEmp import TM_SetupProcessApproverEmp
from TM_SetupProcessApproverDept import TM_SetupProcessApproverDept
from TM_SetupProcessApplyEmp import TM_SetupProcessApplyEmp
from HCSSYS_FunctionListLabel import HCSSYS_FunctionListLabel
from TM_SetupProcess import TM_SetupProcess
from TM_SetupProcessApproveLevel import TM_SetupProcessApproveLevel
from TM_SetupProcessApproverSubstitute import TM_SetupProcessApproverSubstitute
from TM_EmailHR import TM_EmailHR
from TMHP_AssignTargetRequest import TMHP_AssignTargetRequest
from TMPER_TargetKPI import TMPER_TargetKPI
from TMPER_TargetKPI_Emp import TMPER_TargetKPI_Emp
from pymongo.read_concern import ReadConcern
from pymongo.write_concern import WriteConcern
from ..views import *

def create_session():
    session = db_context.db.client.start_session()
    return session
def start_transaction(session):
    session.start_transaction(
        read_concern=ReadConcern("snapshot"),
        write_concern=WriteConcern(w="majority"))
    return session

def abort_transaction(session):
    session.abort_transaction()
    return  session

def end_session(session):
    session.end_session()

def commit_transaction(session):
    session.commit_transaction()