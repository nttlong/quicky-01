# -*- coding: utf-8 -*-
from bson import ObjectId
import qmongo
import models
import common
from Query import AprPeriodEmpOut
import logging
import threading
logger = logging.getLogger(__name__)
global lock
lock = threading.Lock()
import quicky
from bson import SON
from hcs_authorization import action_type,authorization
from collections import OrderedDict

@authorization.authorise(action=action_type.Action.READ)
def get_list_with_searchtext(args):
    searchText = args['data'].get('search', '')
    pageSize = args['data'].get('pageSize', 0)
    pageIndex = args['data'].get('pageIndex', 20)
    sort = args['data'].get('sort', 20)

    pageIndex = (lambda pIndex: pIndex if pIndex != None else 0)(pageIndex)
    pageSize = (lambda pSize: pSize if pSize != None else 20)(pageSize)
    ret=AprPeriodEmpOut.get_empNotApr_by_apr_period(args['data']['apr_period'], args['data']['apr_year'],searchText)
    ret=common.filter_lock(ret, args)
    if(sort != None):
        ret.sort(sort)
    return ret.get_page(pageIndex, pageSize)

@authorization.authorise(action=action_type.Action.READ)
def get_list_distinct_approval_year_and_period(args):
    ret = {}
    collection = common.get_collection('TMPER_AprPeriod').aggregate([
        {"$lookup": {'from': common.get_collection_name_with_schema('SYS_VW_ValueList'), 'localField': 'apr_period',
                     'foreignField': 'value', 'as': 'aprPeriod'}},
        {"$unwind": {'path': '$aprPeriod', "preserveNullAndEmptyArrays": True}},
        {"$match": {
            "$and": [{'aprPeriod.list_name': "LApprovalPeriod"}, {'aprPeriod.language': quicky.language.get_language()}]
        }},
        {"$project": {
            "apr_period_a": {"$ifNull": ["$aprPeriod.caption", ""]},
            "apr_year_a": {'$toString': "$apr_year"},
            "apr_period": {'$toString': "$apr_period"},
            "apr_year": 1
        }},
        {"$project": {
            "caption": {'$concat': ["$apr_year_a", " / ", "$apr_period_a"]},
            "value": {'$concat': ["$apr_year_a", "__", "$apr_period"]},
            "apr_year": 1,
            "apr_period": {'$toInt': "$apr_period"},

        }},
        {"$sort": SON([("apr_year", -1), ("apr_period", -1)])}
    ])

    ret = list(collection)
    ret1 = []
    if (args['data'] != None and args['data'].has_key('apr_period' and 'apr_year')):
        for x in ret:
            if (x['apr_period'] == args['data']['apr_period'] and x['apr_year'] == args['data']['apr_year']):
                continue
            else:
                collection1 = common.get_collection('TMPER_AprPeriodEmpOut').aggregate([
                    {"$match": {
                        "$and": [{'apr_year': x['apr_year']}, {'apr_period': x['apr_period']}]
                    }},
                ])
                if (len(list(collection1)) == 0):
                    ret1.append(x)
        item_list = [e for e in ret if e not in ret1]
        return item_list

def generate(args):
    try:
        lock.acquire()
        ret = {}
        listEmpPerNow = get_EmpDataByPeriodAndYear(args)
        if(len(listEmpPerNow) > 0 and len(args['data']['res']) >0):
            if args['data'] != None and args['data'].has_key('now_apr_period') and args['data'].has_key('now_apr_year') :
                if(args['data'].has_key('chk_exchangeData') and args['data']['chk_exchangeData'] == 1):
                    ret  =   qmongo.models.TMPER_AprPeriodEmpOut.delete("_id in {0}",[ObjectId(x["_id"]) for x in listEmpPerNow])
                    for item in args['data']['res']:
                        item['apr_period'] = args['data']['now_apr_period']
                        item['apr_year'] =  args['data']['now_apr_year']
                        data = set_dict_insert_data(item)
                        ret  = qmongo.models.TMPER_AprPeriodEmpOut.insert(data)
                else:
                    for  item in args['data']['res'] :
                        if item.has_key('apr_period' and 'apr_year' and 'employee_code'):
                            for index, emp in enumerate(listEmpPerNow, start=0):
                                if (item['employee_code'] == emp['employee_code']):
                                     if(emp['department_code'] == None or emp['department_code'] == ""):
                                         emp['department_code'] = item['department_code']
                                     if(emp['job_w_code'] == None or emp['job_w_code'] == ""):
                                         emp['job_w_code'] = item['job_w_code']
                                     if(emp['reason'] == None or emp['reason'] == ""):
                                         emp['reason'] = item['reason']
                                     if(emp['note'] == None or emp['note'] == ""):
                                         emp['note'] = item['note']
                                     data = set_dict_update_data(emp)
                                     ret  = qmongo.models.TMPER_AprPeriodEmpOut.update(
                                                 data, 
                                                "_id == {0}", 
                                                 ObjectId(emp['_id']))
                                     break
                                else:
                                    if(index == len(listEmpPerNow)-1):
                                        item['apr_period'] = args['data']['now_apr_period']
                                        item['apr_year'] =  args['data']['now_apr_year']
                                        data =  set_dict_insert_data(item)
                                        ret  =  qmongo.models.TMPER_AprPeriodEmpOut.insert(data)
                                    else:
                                        continue
                lock.release()
                return ret
        elif(len(listEmpPerNow) == 0 and len(args['data']['res']) >0):
            for item in args['data']['res']:
                item['apr_period'] = args['data']['now_apr_period']
                item['apr_year'] =  args['data']['now_apr_year']
                data = set_dict_insert_data(item)
                ret  =  qmongo.models.TMPER_AprPeriodEmpOut.insert(data)
            lock.release()
            return ret
        lock.release()
        return dict(
            error = "request parameter is not exist"
            )
    except Exception as ex:
        lock.release()
        raise(ex)

@authorization.authorise(action=action_type.Action.WRITE)
def update(args):
    try:
        lock.acquire()
        ret = {}
        if args['data'] != None:
            if(args['data']['tmp']==1):
                del(args['data']['tmp'])
                data =  set_dict_update_data(args['data'])
                ret  =  qmongo.models.TMPER_AprPeriodEmpOut.update(
                    data, 
                    "_id == {0}", 
                    ObjectId(args['data']['_id']))
                lock.release()
                return ret
            else:
                del(args['data']['tmp'])
                data = {
                    "reason":args['data']['reason'],
                    "note":args['data']['note']
                    }
                ret  =  qmongo.models.TMPER_AprPeriodEmpOut.update(
                    data, 
                    "_id in {0}", 
                    [ObjectId(x) for x in args['data']['_id']])
                lock.release()
                return ret
        lock.release()
        return dict(
            error = "request parameter is not exist"
        )
    except Exception as ex:
        lock.release()
        raise(ex)

@authorization.authorise(action=action_type.Action.DELETE)
def delete(args):
    try:
        lock.acquire()
        ret = {}
        if args['data'] != None:
            ret  =  qmongo.models.TMPER_AprPeriodEmpOut.delete("_id in {0}",[ObjectId(x["_id"])for x in args['data']])
            lock.release()
            return ret

        lock.release()
        return dict(
            error = "request parameter is not exist"
        )
    except Exception as ex:
        lock.release()
        raise(ex)

@authorization.authorise(action=action_type.Action.READ)
def get_genPreAperiodData(args):
    if(args['data']!= None):
        ret = {}
        collection = common.get_collection('TMPER_AprPeriodEmpOut').aggregate([
        {"$match":{
            "$and": [ { 'apr_year': int(args['data']['apr_year']) }, { 'apr_period': int(args['data']['apr_period'])} ]
        }},
        {"$project": {
            "apr_period":1,
            "apr_year": 1,
            "employee_code":1,
            "department_code": 1,
            "job_w_code":1,
            "reason":1,
            "note":1
        }},
        #{ "$sort" : SON([("apr_year",-1),("apr_period",-1)]) }
        ])
        ret = list(collection)
        return ret

def get_EmpDataByPeriodYearAndEmp(period, year, emp_code):
    ret = {}
    collection = common.get_collection('TMPER_AprPeriodEmpOut').aggregate([
    {"$match":{
        "$and": [ { 'apr_year': year},
                  { 'apr_period':period  },
                  { 'employee_code': emp_code}]
    }},
    {"$project": {
        "_id":1,
        "apr_period":1,
        "apr_year": 1,
        "employee_code":1,
        "department_code": 1,
        "job_w_code":1,
    }},
    #{ "$sort" : SON([("apr_year",-1),("apr_period",-1)]) }
    ])
    ret = list(collection)
    return (lambda x: x[0] if len(x) > 0 else None)(ret)

def get_EmpDataByPeriodAndYear(args):
    if(args['data']!= None):
        ret = {}
        collection = common.get_collection('TMPER_AprPeriodEmpOut').aggregate([
        {"$match":{
            "$and": [ { 'apr_year': args['data']['now_apr_year'] }, { 'apr_period': args['data']['now_apr_period']} ]
        }},
        {"$project": {
            "apr_period":1,
            "apr_year": 1,
            "employee_code":1,
            "department_code": 1,
            "job_w_code":1,
            "reason":1,
            "note":1
        }},
        #{ "$sort" : SON([("apr_year",-1),("apr_period",-1)]) }
        ])
        ret = list(collection)
        return ret

def get_EmpMultiByEmpcode(emp_code):
    if(emp_code!= ""):
        ret = {}
        collection = common.get_collection('HCSEM_Employees').aggregate([
        {"$match":{'employee_code': emp_code}},
        {"$project": {
            "employee_code":1,
            "department_code": 1,
            "job_w_code":1,
        }},
        ])
        ret = list(collection)
        return (lambda x: x[0] if len(x) > 0 else None)(ret)



def get_insert_multi_empNotApr(args):
    try:
        lock.acquire()
        ret = {}
        if args['data'].has_key('apr_period') and args['data'].has_key('apr_year'):
            apr_period = args['data']['apr_period']
            apr_year = args['data']['apr_year']
            for emp_code in args['data']['list_emp'] :
                item = get_EmpMultiByEmpcode(emp_code)
                item['apr_period'] = apr_period
                item['apr_year'] = apr_year 
                # check item to update or insert data => return item contain "_id and info" of emp_not_apr.
                check_item = get_EmpDataByPeriodYearAndEmp(apr_period,apr_year,emp_code)
                if (check_item != None):
                    data =  set_dict_update_data(check_item)
                    ret  =  qmongo.models.TMPER_AprPeriodEmpOut.update(
                        data, 
                    "_id == {0}", 
                    ObjectId(check_item['_id']))
                else:
                    data =  set_dict_insert_data(item)
                    ret  =  qmongo.models.TMPER_AprPeriodEmpOut.insert(data)
            lock.release()
            return ret
        lock.release()
        return dict(
            error = "request parameter is not exist"
            )
    except Exception as ex:
        lock.release()
        raise(ex)


def set_dict_insert_data(item):
    ret_dict = dict()
    ret_dict.update(
        apr_period         = (lambda x: x['apr_period']        if x.has_key('apr_period')       else None)(item),
        apr_year         = (lambda x: x['apr_year']        if x.has_key('apr_year')       else None)(item),
        employee_code        = (lambda x: x['employee_code']       if x.has_key('employee_code')      else None)(item),
        department_code   = (lambda x: x['department_code']  if x.has_key('department_code') else None)(item),
        job_w_code              = (lambda x: x['job_w_code']             if x.has_key('job_w_code')            else None)(item),
        reason        = (lambda x: x['reason']       if x.has_key('reason')      else None)(item),
        job_working         = (lambda x: x['job_working']        if x.has_key('job_working')       else None)(item),
        note                = (lambda x: x['note']               if x.has_key('note')              else None)(item),
    )
    return ret_dict

def set_dict_update_data(args):
    ret_dict = set_dict_insert_data(args)
    return ret_dict

