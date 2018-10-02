# -*- coding: utf-8 -*-
from bson import ObjectId
import models
from Query import KPIGroup
import logging
import threading
import common
import datetime
logger = logging.getLogger(__name__)
global lock
lock = threading.Lock()

def get_list_email_by_company(args):
    searchText = args['data'].get('search', '')
    pageSize = args['data'].get('pageSize', 0)
    pageIndex = args['data'].get('pageIndex', 20)
    sort = args['data'].get('sort', 20)

    pageIndex = (lambda pIndex: pIndex if pIndex != None else 0)(pageIndex)
    pageSize = (lambda pSize: pSize if pSize != None else 20)(pageSize)
    
    ret = models.TM_EmailHR().aggregate()
    ret.lookup(models.HCSEM_Employees(), "employee_code", "employee_code", "emp")
    ret.unwind("emp", False)
    ret.left_join(models.auth_user_info(), "created_by", "username", "uc")
    ret.left_join(models.auth_user_info(), "modified_by", "username", "um")
    ret.project(
        employee_code = "employee_code",
        full_name="concat(emp.last_name, ' ', emp.first_name)",
        email_address="email_address",
        department_code="department_code",
        note="note",
        created_by="uc.login_account",
        created_on="created_on",
        modified_on="switch(case(modified_on!='',modified_on),'')",
        modified_by="switch(case(modified_by!='',um.login_account),'')"
    )
    ret.match("department_code == {0}", None)

    if (searchText != None):
        ret.match("contains(employee_code, @name) or " + \
                  "contains(full_name, @name) or " + \
                  "contains(email_address, @name) or " + \
                  "contains(note, @name) ", name=searchText.strip())

    if (sort != None):
        ret.sort(sort)

    return ret.get_page(pageIndex, pageSize)

def get_list_email_by_dept(args):
    searchText = args['data'].get('search', '')
    pageSize = args['data'].get('pageSize', 0)
    pageIndex = args['data'].get('pageIndex', 20)
    sort = args['data'].get('sort', 20)

    pageIndex = (lambda pIndex: pIndex if pIndex != None else 0)(pageIndex)
    pageSize = (lambda pSize: pSize if pSize != None else 20)(pageSize)

    ret = models.TM_EmailHR().aggregate()
    ret.lookup(models.HCSEM_Employees(), "employee_code", "employee_code", "emp")
    ret.unwind("emp", False)
    ret.lookup(models.HCSSYS_Departments(), "department_code", "department_code", "dept")
    ret.unwind("dept", False)
    ret.left_join(models.auth_user_info(), "created_by", "username", "uc")
    ret.left_join(models.auth_user_info(), "modified_by", "username", "um")
    ret.project(
        employee_code="employee_code",
        full_name="concat(emp.last_name, ' ', emp.first_name)",
        email_address="email_address",
        department_code="department_code",
        level_code = "dept.level_code",
        note="note",
        created_by="uc.login_account",
        created_on="created_on",
        modified_on="switch(case(modified_on!='',modified_on),'')",
        modified_by="switch(case(modified_by!='',um.login_account),'')"
    ).match('department_code != {0}', None)
    if args['data'].has_key('department_code'):
        ret.match("level_code == {0}", args['data']['department_code'])

    if (searchText != None):
        ret.match("contains(employee_code, @name) or " + \
                  "contains(full_name, @name) or " + \
                  "contains(email_address, @name) or " + \
                  "contains(note, @name) ", name=searchText.strip())

    if (sort != None):
        ret.sort(sort)

    return ret.get_page(pageIndex, pageSize)

def check_using_dept(args):
    find = models.TM_EmailHR().aggregate().project(
        employee_code = 1,
        department_code = 1
    ).match("employee_code in @employee_code and department_code != @department_code", employee_code = args['data'], department_code = None).get_list()

    return {"exist":(lambda x: True if x > 0 else False)(len(find))}

def check_using_by_com(args):
    find = models.TM_EmailHR().aggregate().project(
        employee_code = 1,
        department_code = 1
    ).match("employee_code in @employee_code and department_code == @department_code", employee_code = args['data'], department_code = None).get_list()

    return {"exist":(lambda x: True if x > 0 else False)(len(find))}

def insert(args):
    try:
        find = models.TM_EmailHR().aggregate().lookup(models.HCSEM_Employees(), "employee_code", "employee_code", "emp").project(
            employee_code = "employee_code",
            email = "switch(case(emp.email!='',emp.email),'')"
        ).match("employee_code in @employee_code and department_code == @department_code", employee_code = args['data'], department_code = None).get_list()

        lst_emp = args['data']
        list_insert = [item for item in lst_emp if item not in [x['employee_code'] for x in find]]

        dict_insert = []
        import HCSEM_Employees
        for x in lst_emp:
            if x in list_insert:
                dict_insert.append({
                    "email": HCSEM_Employees.get_employee_by_emp_code({"data":{"employee_code":x}}).get("email", ""),
                    "employee_code": x,
                    "department_code": None,
                    "modified_on": None,
                    "modified_by": None,
                    "created_on": datetime.datetime.now(),
                    "created_by": common.get_user_id()
                })

        rs = common.get_collection("TM_EmailHR").insert_many(dict_insert)

        ret = {}
        if rs.acknowledged == True:
            ret = {
                "error": None,
                "inserted_ids": rs.inserted_ids,
            }
        else:
            ret = {
                "error": "have error when insert"
            }

        return ret

    except Exception as ex:
        raise (ex)

def insert_force(args):
    emp_codes = args['data']

    find = models.HCSEM_Employees().aggregate().project(
        employee_code=1,
        email=1
    ).match("employee_code in {0}", emp_codes).get_list()

    deleted = models.TM_EmailHR().delete("employee_code in {0}", emp_codes)

    ret = None

    try:
        rs = common.get_collection("TM_EmailHR").insert_many(
            [{
                "employee_code": x["employee_code"],
                "email_address": x["email"],
                "note": None,
                "department_code": None,
                "modified_on": None,
                "modified_by": None,
                "created_on": datetime.datetime.now(),
                "created_by": common.get_user_id()
            } for x in find]
        )

        if rs.acknowledged == True:
            ret = {
                "error": None,
                "inserted_ids": rs.inserted_ids,
            }
        else:
            ret = {
                "error": "have error when insert"
            }
    except Exception as ex:
        ret = {
            "error": ex.message
        }

    return ret

def update(args):
    emp_code = args['data']['employee_code']
    del args['data']['employee_code']
    args['data']['modified_on'] = datetime.datetime.now()
    args['data']['modified_by'] = common.get_user_id()
    rs = models.TM_EmailHR().update(args['data'], "employee_code == {0}", emp_code)

    return rs

def delete(args):
    rs = models.TM_EmailHR().delete("employee_code in {0}", [x["employee_code"] for x in args['data']])
    return rs

def insert_dept(args):
    try:
        find = models.TM_EmailHR().aggregate().lookup(models.HCSEM_Employees(), "employee_code", "employee_code", "emp").project(
            employee_code = "employee_code",
            email = "switch(case(emp.email!='',emp.email),'')",
            department_code = "department_code"
        ).match("employee_code in @employee_code and department_code != @department_code", employee_code = args['data']['list'], department_code = None).get_list()

        lst_emp = args['data']['list']
        list_insert = [item for item in lst_emp if item not in [x['employee_code'] for x in find]]

        dict_insert = []
        import HCSEM_Employees
        for x in lst_emp:
            if x in list_insert:
                dict_insert.append({
                    "email": HCSEM_Employees.get_employee_by_emp_code({"data":{"employee_code":x}}).get("email", ""),
                    "employee_code": x,
                    "department_code": args['data']['department_code'],
                    "modified_on": None,
                    "modified_by": None,
                    "created_on": datetime.datetime.now(),
                    "created_by": common.get_user_id()
                })

        rs = common.get_collection("TM_EmailHR").insert_many(dict_insert)

        ret = {}
        if rs.acknowledged == True:
            ret = {
                "error": None,
                "inserted_ids": rs.inserted_ids,
            }
        else:
            ret = {
                "error": "have error when insert"
            }

        return ret
    except Exception as ex:
        raise(ex)

def insert_force_dept(args):
    emp_codes = args['data']['list']

    find = models.HCSEM_Employees().aggregate().project(
        employee_code=1,
        email=1
    ).match("employee_code in {0}", emp_codes).get_list()

    deleted = models.TM_EmailHR().delete("employee_code in {0}", emp_codes)

    ret = None

    try:
        rs = common.get_collection("TM_EmailHR").insert_many(
            [{
                "employee_code": x["employee_code"],
                "email_address": x["email"],
                "note": None,
                "department_code": args['data']['department_code'],
                "modified_on": None,
                "modified_by": None,
                "created_on": datetime.datetime.now(),
                "created_by": common.get_user_id()
            } for x in find]
        )

        if rs.acknowledged == True:
            ret = {
                "error": None,
                "inserted_ids": rs.inserted_ids,
            }
        else:
            ret = {
                "error": "have error when insert"
            }
    except Exception as ex:
        ret = {
            "error": ex.message
        }

    return ret