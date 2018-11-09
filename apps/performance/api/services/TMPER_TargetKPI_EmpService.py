# -*- coding: utf-8 -*-
from .. import models
from .. import common
import qmongo


def get_list_giao(args):
    ret = None
    qr = None
    dept_code = args['data'].get("department_code", None)
    job_code = args['data'].get("job_w_code", None)
    match_qr = {}

    if dept_code != None and len(dept_code) > 0:
        match_qr.update(department_code = {"$in": dept_code})
    if job_code != None and len(job_code) > 0:
        match_qr.update(job_w_code={"$in": job_code})

    current_period = list(common.get_collection("TMPER_AprPeriod").find({
        "apr_year": args['data']['apr_year'],
        "apr_period": args['data']['apr_period']
    }))[0]

    if args['data']['status'] == 1:
        qr = common.get_collection('TMPER_TargetKPI_Emp').aggregate([
            {"$match":{
                "apr_year": args['data']['apr_year'],
                "apr_period": args['data']['apr_period']
            }},
            {"$lookup":{
                "from": common.get_collection_name_with_schema('HCSEM_Employees'),
                "localField": "employee_code",
                "foreignField": "employee_code",
                "as": "emp"
            }},
            {"$unwind":{
                "path": "$emp",
                "preserveNullAndEmptyArrays": False
            }},
            {"$lookup":{
                "from": common.get_collection_name_with_schema('HCSLS_JobWorking'),
                "localField": "emp.job_w_code",
                "foreignField": "job_w_code",
                "as": "jk"
            }},
            {"$unwind": {
                "path": "$jk",
                "preserveNullAndEmptyArrays": True
            }},
            {"$project":{
                "rec_id": "$rec_id",
                "employee_name": {"$concat":["$emp.last_name", " ", "$emp.first_name"]},
                "employee_code": "$employee_code",
                "job_working": {"$ifNull": ["$jk.job_w_name", ""]},
                "join_date": "$emp.join_date",
                "department_code": "$emp.department_code",
                "job_w_code": "$jk.job_w_code",
                "give_over": {"$gt": [ "$assign_date", current_period['give_target_to']]},
                "approve_and_edit": {"$eq":["$is_modified", 2]}
            }},
            {"$match":match_qr}
        ])
    elif args['data']['status'] == 2:
        qr = common.get_collection('TMHP_AssignTargetRequest').aggregate([
            {"$match": {
                "apr_year": args['data']['apr_year'],
                "apr_period": args['data']['apr_period'],
                "request_status": 1
            }},
            {"$lookup": {
                "from": common.get_collection_name_with_schema('HCSEM_Employees'),
                "localField": "employee_code",
                "foreignField": "employee_code",
                "as": "emp"
            }},
            {"$unwind": {
                "path": "$emp",
                "preserveNullAndEmptyArrays": False
            }},
            {"$lookup": {
                "from": common.get_collection_name_with_schema('HCSLS_JobWorking'),
                "localField": "emp.job_w_code",
                "foreignField": "job_w_code",
                "as": "jk"
            }},
            {"$unwind": {
                "path": "$jk",
                "preserveNullAndEmptyArrays": True
            }},
            {"$project": {
                "employee_name": {"$concat": ["$emp.last_name", " ", "$emp.first_name"]},
                "employee_code": "$employee_code",
                "job_working": {"$ifNull": ["$jk.job_w_name", ""]},
                "join_date": "$emp.join_date",
                "department_code": "$emp.department_code",
                "job_w_code": "$jk.job_w_code",
                "give_over": {"$gt": ["$assign_date", current_period['give_target_from']]},
                "approve_and_edit": {"$literal": False}
            }},
            {"$match":match_qr}
        ])
    elif args['data']['status'] == 3:
        data_in_kpi_emp = list(common.get_collection("TMPER_TargetKPI_Emp").find({
                    "apr_year": args['data']['apr_year'],
                    "apr_period": args['data']['apr_period']
                }))
        qr = common.get_collection('HCSEM_Employees').aggregate([
            {"$match":{
                "employee_code": {"$nin": [x['employee_code'] for x in data_in_kpi_emp]}
            }},
            {"$lookup": {
                "from": common.get_collection_name_with_schema('HCSLS_JobWorking'),
                "localField": "job_w_code",
                "foreignField": "job_w_code",
                "as": "jk"
            }},
            {"$unwind": {
                "path": "$jk",
                "preserveNullAndEmptyArrays": True
            }},
            {"$project": {
                "_id": 0,
                "employee_name": {"$concat": ["$last_name", " ", "$first_name"]},
                "employee_code": "$employee_code",
                "job_working": {"$ifNull": ["$jk.job_w_name", ""]},
                "join_date": "$join_date",
                "department_code": "$department_code",
                "job_w_code": "$jk.job_w_code",
                "over": {"$literal": False},
                "approve_and_edit": {"$literal": False}
            }},
            {"$match":match_qr}
        ])
    else:
        qr = None

    if qr != None:
        return (lambda x: x if len(x) > 0 else [])(list(qr))
    return []

def get_list_employee_in_apr_period(args, is_paging = True):
    searchText = args['data'].get('search', '')
    pageSize = args['data'].get('pageSize', 0)
    pageIndex = args['data'].get('pageIndex', 20)
    sort = args['data'].get('sort', 20)

    pageIndex = (lambda pIndex: pIndex if pIndex != None else 0)(pageIndex)
    pageSize = (lambda pSize: pSize if pSize != None else 20)(pageSize)
    search = (lambda x: x.strip() if searchText != None else "")(searchText)

    begin_end_date = common.get_start_end_apr_period_date(args['data']['apr_period'], args['data']['apr_year'])
    employee_not_apr = []
    result = []

    temp = list(common.get_collection('HCSEM_Employees').aggregate([
                        {"$match":{
                            "join_date": {"$lt": begin_end_date['end_apr_period']},
                            "$or":[{"end_date": {"$eq": None}}, {"end_date": {"$gt": begin_end_date['begin_apr_period']}}]
                        }},
                        {"$project":{
                            "_id": 0,
                            "employee_code": 1
                        }}
                    ]))

    total_employee = [x['employee_code'] for x in temp]

    process_level_apply_for = qmongo.models.TM_SetupProcess.aggregate.project(
        process_id = 1,
        process_level_apply_for = 1
    ).match("process_id == '2'").get_item()['process_level_apply_for']

    if process_level_apply_for == None:
        raise Exception('Setup process is error')
    elif process_level_apply_for == 1:
        qr = qmongo.models.TMPER_AprPeriodEmpOut.aggregate.project(
            _id=0,
            apr_year=1,
            apr_period=1,
            employee_code=1
        ).match("apr_period == @period and apr_year == @year",
                period=args['data']['apr_period'],
                year=args['data']['apr_year']).get_list()

        _list = [x['employee_code'] for x in qr]

        result = [i for i in total_employee if i not in _list]
    elif process_level_apply_for == 2:
        qr = qmongo.models.TMPER_AprPeriodEmpOut.aggregate.project(
            _id=0,
            apr_year=1,
            apr_period=1,
            employee_code=1
        ).match("apr_period == @period and apr_year == @year",
                period=args['data']['apr_period'],
                year=args['data']['apr_year']).get_list()

        _list = [x['employee_code'] for x in qr]

        qr_emp_360 = qmongo.models.TM_SetupProcessApplyEmp.aggregate.project(
            process_id=1,
            employee_code=1
        ).match("process_id == @id", id="3").get_list()

        list_emp_360 = [x['employee_code'] for x in qr_emp_360]

        result = [i for i in total_employee if i not in _list and i not in list_emp_360]
    elif process_level_apply_for == 3:
        qr = qmongo.models.TM_SetupProcessApplyEmp.aggregate.project(
            process_id = 1,
            employee_code = 1
        ).match("process_id == @id", id = "2").get_list()

        result = [x['employee_code'] for x in qr]



    ret = qmongo.models.HCSEM_Employees.aggregate.left_join(
        models.HCSLS_JobWorking(),
        "job_w_code",
        "job_w_code",
        "jk"
    ).project(
        employee_code = "employee_code",
        employee_name = "concat(last_name, ' ', first_name)",
        job_w_name = "jk.job_w_name",
    ).match(
        "employee_code not in @code", code = result
    )

    if is_paging == False:
        return ret.get_list()

    if (search != None and search != ""):
        ret.match("contains(employee_name, @name) or contains(job_w_name, @name)", name=search.strip())

    if (sort != None):
        ret.sort(sort)

    if is_paging == True:
        return ret.get_page(pageIndex, pageSize)

def count_employee_with_status_give_target(args):
    result = {
        'approved': 0,
        'waiting': 0,
        'not_give': 0
    }

    result['approved'] = common.get_collection('TMPER_TargetKPI_Emp').find({
        "apr_period": args['data']['apr_period'],
        "apr_year": args['data']['apr_year']
    }).count()
    result['waiting'] = common.get_collection('TMHP_AssignTargetRequest').find({
        "request_status": 1,
        "apr_period": args['data']['apr_period'],
        "apr_year": args['data']['apr_year']
    }).count()
    result['not_give'] = get_list_employee_in_apr_period({"data":{
        "apr_period":args['data']['apr_period'],
        "apr_year":args['data']['apr_year']
    }}, False).__len__() - (result['approved'] + result['waiting'])

    return result