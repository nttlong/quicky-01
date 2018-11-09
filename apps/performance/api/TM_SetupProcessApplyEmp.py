# -*- coding: utf-8 -*-
import models
import datetime
import common
import qmongo
def get_list_by_mode(args):

    searchText = args['data'].get('search', '')
    pageSize = args['data'].get('pageSize', 0)
    pageIndex = args['data'].get('pageIndex', 20)
    sort = args['data'].get('sort', {})

    pageIndex = (lambda pIndex: pIndex if pIndex != None else 0)(pageIndex)
    pageSize = (lambda pSize: pSize if pSize != None else 20)(pageSize)

    collection = qmongo.models.TM_SetupProcessApplyEmp.aggregate
    collection.join(qmongo.models.HCSEM_Employees, "employee_code", "employee_code", "emp")
    collection.join(qmongo.models.HCSSYS_Departments, "emp.department_code", "department_code", "dept")
    collection.left_join(qmongo.models.HCSLS_JobWorking, "emp.job_w_code", "job_w_code", "jk")
    collection.left_join(qmongo.models.HCSLS_JobWorkingGroup, "jk.gjw_code", "gjw_code", "gjk")
    collection.project(
        process_id="process_id",
        employee_code="employee_code",
        email="switch(case(emp.email!='',emp.email),'')",
        join_date="emp.join_date",
        employee_name="concat(emp.last_name, ' ', emp.first_name)",
        department_name = "dept.department_name",
        job_w_name= "switch(case(jk.job_w_name!='',jk.job_w_name),'')",
        job_w_code= "switch(case(jk.job_w_code!='',jk.job_w_code),'')",
        department_code="emp.department_code",
        job_working_level = "gjk.level_code",
        dept_level="dept.level_code",
        gjw_code="switch(case(jk.gjw_code!='',jk.gjw_code),'')"
    ).match('process_id == {0}', args['data']['process_id'])

    if args['data'].has_key('mode') and args['data']['mode'] == 0:
        collection.match("job_working_level == {0}", args['data']['code'])
    elif args['data'].has_key('mode') and args['data']['mode'] == 1:
        collection.match("dept_level == {0}", args['data']['code'])

    if (searchText != None):
        collection.match("contains(employee_code, @name) or contains(employee_name, @name)" + \
                  "or contains(department_name, @name) or contains(job_w_name, @name) " + \
                  "or contains(join_date, @name) or contains(email, @name)", name=searchText.strip())

    if (sort != None):
        collection.sort(sort)

    data = collection.get_page(pageIndex, pageSize)

    return data

def get_list_employee_in_current_process_and_process_360(args):
    try:
        process_in = ["3"]
        process_in.append(args['data']['process_id'])
        ret =qmongo.models.TM_SetupProcessApplyEmp.aggregate.project(
            process_id = 1,
            employee_code = 1
        ).match("process_id in {0}", process_in)
        result = [x['employee_code'] for x in ret.get_list()]
        return result
    except Exception as ex:
        raise ex

def insert(args):
    try:
        ret = qmongo.models.TM_SetupProcessApplyEmp.insert(
            args['data']
        )
        return ret
    except Exception as ex:
        raise ex

def get_list_selected_employee(args):
    from Query import Employee

    list_emp_appr = qmongo.models.TM_SetupProcessApproverEmp.aggregate.project(
        employee_code = 1,
        process_id = 1
    ).match("process_id == {0}", args['data']['process_id']).get_list()

    seleted_employee = Employee.get_employee_by_employee_codes(args['data']['employee_codes'])
    result = [x for x in seleted_employee if x['employee_code'] not in [y['employee_code'] for y in list_emp_appr]]

    return result

def get_list_by_process_id(args):
    ret =qmongo.models.TM_SetupProcessApproverEmp.aggregate.project(
        process_id=1,
        approve_level=1,
        employee_code=1,
        appover_code=1
    ).join(qmongo.models.HCSEM_Employees, "employee_code", "employee_code", "emp")\
    .project(
        process_id="process_id",
        approve_level="approve_level",
        employee_code="employee_code",
        appover_code="appover_code",
        employee_name="concat(emp.last_name, ' ', emp.first_name)",
        first_name="emp.first_name",
        last_name="emp.last_name",
        department_code="emp.department_code"
    ).join(qmongo.models.HCSSYS_Departments, "department_code", "department_code", "dept")\
    .project(
        process_id="process_id",
        approve_level="approve_level",
        employee_code="employee_code",
        appover_code="appover_code",
        employee_name="employee_name",
        department_code="department_code",
        first_name="first_name",
        last_name="last_name",
        department_name="dept.department_name"
    ).match("process_id == {0}", args['data']['process_id']).get_list()

    return ret

def insert_by_emp(args):
    list_insert = []

    try:
        for x in args['data']['employee_code']:
            list_insert.append({
                'employee_code' : x,
                'approve_level' : args['data']['level'],
                'process_id' : args['data']['process_id'],
                'appover_code' : args['data']['appover_code']
            })
        ret = None
        if len(list_insert) > 0:
            #ret = common.get_collection('TM_SetupProcessApproverEmp').insert_many(list_insert)
            ret =qmongo.models.TM_SetupProcessApproverEmp.insert(list_insert)

        return ret

    except Exception as ex:
        raise ex

def update_by_emp(args):
    list_update = []
    list_employee = qmongo.models.TM_SetupProcessApproverEmp.aggregate.project(
        process_id=1,
        approve_level=1,
        employee_code=1,
        appover_code=1
    ).match("process_id == @process_id and employee_code in @emp_code",
            process_id = args['data']['process_id'],
            emp_code = args['data']['employee_code']).get_list()

    try:
        for x in args['data']['employee_code']:
            currentEmp = filter(lambda emp: emp['employee_code'] == x, list_employee)
            if currentEmp != None and len(currentEmp) > 0:
                approve_code_update = []
                for y in args['data']['appover_code']:
                    if(y['checked'] == True):
                        approve_code_update.append(y['appover_code'])
                    else:
                        approve_code_update.append(currentEmp[0]['appover_code'][args['data']['appover_code'].index(y)])

                list_update.append({
                    'employee_code': x,
                    'approve_level': args['data']['level'],
                    'process_id': args['data']['process_id'],
                    'appover_code': approve_code_update
                })
        ret = None
        result = []
        if len(list_update) > 0:
            for x in list_update:
                ret = qmongo.models.TM_SetupProcessApproverEmp.update({
                    'appover_code' : x['appover_code']
                }, "process_id == @process_id and employee_code == @emp_code",
                process_id = x["process_id"],
                emp_code = x["employee_code"])
                result.append(ret)

        return result

    except Exception as ex:
        raise ex

def delete_emp(args):
    try:
        ret = {}
        if args['data'] != None:
            ret  =  qmongo.models.TM_SetupProcessApproverEmp.delete("process_id == @process_id and employee_code in @emp_code",
                                                               process_id = args['data']['process_id'],
                                                               emp_code = args['data']['employee_code'])
            return ret

        return dict(
            error = "request parameter is not exist"
        )
    except Exception as ex:
        raise(ex)