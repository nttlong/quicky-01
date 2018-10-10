# -*- coding: utf-8 -*-
from bson import ObjectId
import models
import common
global lock
import threading
lock = threading.Lock()
import datetime
#import TM_SetupProcessApproveLevel

def get_list_with_process_id(args):
    try:
        if args['data'] != None and args['data'].has_key('process_id'):
            items = models.TM_SetupProcessApproverSubstitute().aggregate().project(
                process_id=1,
                process_code=1,
                substitute_code=1,
                from_date=1,
                to_date=1,
                note=1
                ).match("process_id == {0}", args['data']['process_id'])
        return items.get_item()
        raise(Exception("not found process_id"))
    except Exception as ex:
        raise(ex)

def get_list_with_searchtext(args):
    searchText = args['data'].get('search', '')
    pageSize = args['data'].get('pageSize', 0)
    pageIndex = args['data'].get('pageIndex', 20)
    sort = args['data'].get('sort', 20)

    pageIndex = (lambda pIndex: pIndex if pIndex != None else 0)(pageIndex)
    pageSize = (lambda pSize: pSize if pSize != None else 20)(pageSize)

    items = models.TM_SetupProcessApproverSubstitute().aggregate()
    items.left_join(models.HCSEM_Employees(), "process_code", "employee_code", "emp")
    items.left_join(models.HCSEM_Employees(), "substitute_code", "employee_code", "em")
    items.left_join(models.auth_user_info(), "created_by", "username", "uc")
    items.left_join(models.auth_user_info(), "modified_by", "username", "um")
    items.project(
        process_id=1,
        process_code=1,
        substitute_code=1,
        from_date=1,
        to_date=1,
        note=1,
        created_by="uc.login_account",
        created_on="created_on",
        modified_on="switch(case(modified_on!='',modified_on),'')",
        modified_by="switch(case(modified_by!='',um.login_account),'')",
        process_name="concat(emp.last_name, ' ', emp.first_name)",
        substitute_name="concat(em.last_name, ' ', em.first_name)",
    )

    items.match("process_id == {0}", args['data']['process_id'])

    if(searchText != None) :
        items.match("contains(process_code, @name) or contains(process_name, @name) or " + \
                    "contains(substitute_code, @name) or contains(substitute_name, @name) or " + \
                    "contains(frsend_email_once_from_hourom_date, @name) or contains(to_date, @name)", name=searchText)

    if(sort != None):
        items.sort(sort)
        
    return items.get_page(pageIndex, pageSize)

def insert(args):
    # if args['data'] != None:
    #     ret = models.TM_SetupProcessApproverSubstitute().insert(args['data'])
    #     return ret
    # return None
    try:
        lock.acquire()
        ret = {}
        if args['data'] != None:
            data =  set_dict_insert_data(args)
            ret  =  models.TM_SetupProcessApproverSubstitute().insert(data)
            lock.release()
            return ret

        lock.release()
        return dict(
            error = "request parameter is not exist"
        )
    except Exception as ex:
        lock.release()
        raise(ex)

def save(args):
    try:
        lock.acquire()
        ret = {}
        if args['data'] != None:
            data =  set_dict_insert_data(args)
            ret  =  models.TM_SetupProcessApproverSubstitute().insert(data)
            lock.release()
            return ret
        lock.release()
        return dict(
            error = "request parameter is not exist"
        )
    except Exception as ex:
        lock.release()
        raise(ex)

def update(args):
    process_id = ""
    if args['data'] != None:
        if args['data']['process_id'] == None:
            return None
        else:
            if (args['data'].has_key('process_id')):
                process_id = args['data']['process_id']
                args['data'].pop('process_id')
            ret = models.TM_SetupProcessApproverSubstitute().update(
                args['data'],
                "process_id==@process_id",
                dict(
                    process_id=process_id
                ))
            return ret
    return None

def delete(args):
    if args['data'] != None:
        # ret = models.TM_SetupProcessApproverSubstitute().delete("process_code in {0}", [x["process_code"] for x in args['data']])
        ret = models.TM_SetupProcessApproverSubstitute().delete(
            "_id in {1}",
            args['data']['process_id'],
            [ObjectId(x) for x in args['data']['_id']])
        return ret
    return None

def set_dict_insert_data(args):
    data = dict()
    data.update(
        process_id =  args['data']['process_id'],
        process_code     =     (lambda x: x['process_code'] if x.has_key('process_code') else None)(args['data']),
        substitute_code    =     (lambda x: x['substitute_code'] if x.has_key('substitute_code') else None)(args['data']),
        from_date    =     (lambda x: x['from_date'] if x.has_key('from_date') else None)(args['data']),
        to_date    =     (lambda x: x['to_date'] if x.has_key('to_date') else None)(args['data']),
        note         =     (lambda x: x['note'] if x.has_key('note') else None)(args['data']),
    )
    return data


