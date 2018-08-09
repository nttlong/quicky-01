from qmongo import qview
from quicky import tenancy
from ..models.HCSEM_Employees import HCSEM_Employees

def SYS_VW_ValueList():
    return qview.create_mongodb_view(
        models.SYS_ValueList().aggregate().unwind("values")
        ,
        "SYS_VW_ValueList"
        )

def HCSEM_VW_EmployeeCBCC():
    return qview.create_mongodb_view(
            HCSEM_Employees().aggregate().project(
            employee_code =  1,
            first_name =  1,
            last_name =  1,
            is_cbcc =  1,
            full_name =  "concat(last_name, ' ', first_name)"
            ).match('is_cbcc == {0}', True)
        ,
        "HCSEM_VW_EmployeeCBCC"
        )