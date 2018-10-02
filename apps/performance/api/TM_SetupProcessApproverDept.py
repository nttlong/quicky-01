# -*- coding: utf-8 -*-
import models
import datetime
import common

def get_list_process_approve_by_dept(args):

    searchText = args['data'].get('search', '')
    pageSize = args['data'].get('pageSize', 0)
    pageIndex = args['data'].get('pageIndex', 20)
    sort = args['data'].get('sort', 20)

    pageIndex = (lambda pIndex: pIndex if pIndex != None else 0)(pageIndex)
    pageSize = (lambda pSize: pSize if pSize != None else 20)(pageSize)

    collection = models.TM_SetupProcessApproverDept().aggregate()
    collection.join(models.HCSSYS_Departments(), "department_code", "department_code", "dept")
    collection.project(
        process_id = "process_id",
        approve_level = "approve_level",
        department_code = "department_code",
        appover_code = "appover_code",
        department_name = "dept.department_name"
    ).match('process_id == {0}', args['data']['process_id'])

    data = collection.get_page(pageIndex, pageSize)

    if(len(data["items"]) > 0):
        result_data = []
        for x in data['items']:
            record = dict()

            record.update(
                process_id = x["process_id"],
                approve_level=x["approve_level"],
                department_code=x["department_code"],
                department_name=x["department_name"],
                approve_level_1 = x['appover_code'][0],
                approve_level_2 = x['appover_code'][1],
                approve_level_3 = x['appover_code'][2],
                approve_level_4 = x['appover_code'][3],
                approve_level_5 = x['appover_code'][4],
                approve_level_6 = x['appover_code'][5],
                approve_level_7 = x['appover_code'][6],
                approve_level_8 = x['appover_code'][7],
                approve_level_9 = x['appover_code'][8],
                approve_level_10 = x['appover_code'][9],
                approve_level_11 = x['appover_code'][10],
                approve_level_12 = x['appover_code'][11],
                approve_level_13 = x['appover_code'][12],
                approve_level_14 = x['appover_code'][13],
                approve_level_15 = x['appover_code'][14],
                approve_level_16 = x['appover_code'][15],
                approve_level_17 = x['appover_code'][16],
                approve_level_18 = x['appover_code'][17],
                approve_level_19 = x['appover_code'][18],
                approve_level_20 = x['appover_code'][19]
            )

            result_data.append(record)

        data['items'] = result_data

    return data

def get_list_by_process_id(args):
    ret = models.TM_SetupProcessApproverDept().aggregate()\
    .project(
        process_id = 1,
        department_code = 1,
    ).match("process_id == {0}", args['data']['process_id']).get_list()

    return ret

def insert_by_dept(args):
    list_insert = []

    try:
        for x in args['data']['department_code']:
            list_insert.append({
                'department_code' : x,
                'approve_level' : args['data']['level'],
                'process_id' : args['data']['process_id'],
                'appover_code' : args['data']['appover_code']
            })
        ret = None
        if len(list_insert) > 0:
            ret = models.TM_SetupProcessApproverDept().insert(list_insert)

        return ret

    except Exception as ex:
        raise ex

def update_by_dept(args):
    list_update = []
    list_department = models.TM_SetupProcessApproverDept().aggregate().project(
        process_id=1,
        approve_level=1,
        department_code=1,
        appover_code=1
    ).match("process_id == @process_id and department_code in @dept_code",
            process_id = args['data']['process_id'],
            dept_code = args['data']['department_code']).get_list()

    try:
        for x in args['data']['department_code']:
            currentDept = filter(lambda emp: emp['department_code'] == x, list_department)
            if currentDept != None and len(currentDept) > 0:
                approve_code_update = []
                for y in args['data']['appover_code']:
                    if(y['checked'] == True):
                        approve_code_update.append(y['appover_code'])
                    else:
                        approve_code_update.append(currentDept[0]['appover_code'][args['data']['appover_code'].index(y)])

                list_update.append({
                    'department_code': x,
                    'approve_level': args['data']['level'],
                    'process_id': args['data']['process_id'],
                    'appover_code': approve_code_update
                })
        ret = None
        result = []
        if len(list_update) > 0:
            for x in list_update:
                ret = models.TM_SetupProcessApproverDept().update({
                    'appover_code' : x['appover_code']
                }, "process_id == @process_id and department_code == @dept_code",
                process_id = x["process_id"],
                    dept_code = x["department_code"])
                result.append(ret)

        return result

    except Exception as ex:
        raise ex

def delete_dept(args):
    try:
        ret = {}
        if args['data'] != None:
            ret  =  models.TM_SetupProcessApproverDept().delete("process_id == @process_id and department_code in @department_code",
                                                                process_id = args['data']['process_id'],
                                                                department_code = args['data']['department_code'])
            return ret

        return dict(
            error = "request parameter is not exist"
        )
    except Exception as ex:
        raise(ex)