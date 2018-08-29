# -*- coding: utf-8 -*-
from bson import ObjectId
import models
from Query import KPI
import logging
import datetime
import threading
import common
logger = logging.getLogger(__name__)
global lock
lock = threading.Lock()

def get_list_with_searchtext(args):
    searchText = args['data'].get('search', '')
    pageSize = args['data'].get('pageSize', 0)
    pageIndex = args['data'].get('pageIndex', 20)
    sort = args['data'].get('sort', 20)

    pageIndex = (lambda pIndex: pIndex if pIndex != None else 0)(pageIndex)
    pageSize = (lambda pSize: pSize if pSize != None else 20)(pageSize)

    collection = common.get_collection('TMLS_KPI')
    ret = collection.aggregate([
    {'$lookup': {
        'foreignField': 'value', 
        'as': 'val', 
        'from': common.get_collection_name_with_schema('SYS_VW_ValueList'),
        'localField': 'cycle_type'
        }
    }, 
    {'$unwind': {
        'path': '$val', 
        'preserveNullAndEmptyArrays': True
        }
    }, 
    {'$match': {   
        '$and':[{
                    '$or' :[{ 'val.list_name':None},
                            { 'val.list_name':'LCycleType'}]
                },
                {
                    '$or' :[{ 'val.language':None},
                            { 'val.language': common.get_language()}]
                }]
        }
    },
    {'$lookup': {
        'foreignField': 'unit_code', 
        'as': 'unit', 
        'from': common.get_collection_name_with_schema('HCSLS_Unit'), 
        'localField': 'unit_code'
        }
    }, 
    {'$unwind': {
        'path': '$unit', 
        'preserveNullAndEmptyArrays': True
        }
    }, 
    {'$lookup': {
        'foreignField': 'kpi_group_code', 
        'as': 'kpig', 
        'from': common.get_collection_name_with_schema('TMLS_KPIGroup'), 
        'localField': 'kpi_group_code'
        }
    }, 
    {'$unwind': {
        'path': '$kpig', 
        'preserveNullAndEmptyArrays': True
        }
    }, 
    {'$project': {
        'kpi_name': '$kpi_name', 
        'is_apply_all': '$is_apply_all', 
        'kpi_desc': '$kpi_desc', 
        'cycle_type': { '$ifNull': [ '$val.caption', '' ] }, 
        'kpi_code': '$kpi_code', 
        'level_code': '$kpig.level_code',
        'weight': '$weight', 
        'unit_code': { '$ifNull': [ '$unit.unit_name', '' ] }, 
        'lock': '$lock', 
        'benchmark': { '$ifNull': [ '$benchmark', '' ] }
        }
    }, 
    {'$match': {'lock': common.aggregate_filter_lock(args['data']['lock']), 'level_code':{'$eq':args['data']['kpi_group_code']}}}, 
    {'$sort': common.aggregate_sort(sort)},
    {"$facet": {
           "metadata": [{ "$count": "total" }, { "$addFields": { "page_index": pageIndex, "page_size": pageSize } }],
           "data": [{ "$skip": pageSize * pageIndex }, { "$limit": pageSize }]
       }
    },
    {"$unwind": { "path": '$metadata', "preserveNullAndEmptyArrays": False }},
    {"$project": {
            'page_size': '$metadata.page_size',
            'page_index': '$metadata.page_index',
            'total_items': '$metadata.total',
            'items': '$data'
        }
    }])

    return (lambda x: x[0] if x != None and len(x) > 0 else {
        'page_size': pageSize,
        'page_index': pageIndex,
        'total_items': 0,
        'items': []
        })(list(ret))

def get_by_kpi_code(args):
    try:
        ret = models.TMLS_KPI().aggregate()
        ret.lookup(models.HCSLS_VW_JobWorkingKPI(), "kpi_code", "kpi_code", "j_kpi")
        ret.left_join(models.auth_user_info(), "created_by", "username", "uc")
        ret.left_join(models.auth_user_info(), "modified_by", "username", "um")
        ret.project(
            kpi_code = "kpi_code",
            kpi_name = "kpi_name",
            kpi_name2 = "kpi_name2",
            job_working = "j_kpi.job_w_code",
            kpi_group_code = "kpi_group_code",
            unit_code = "unit_code",
            cycle_type = "cycle_type",
            kpi_desc = "kpi_desc",
            kpi_ref = "kpi_ref",
            weight = "weight",
            benchmark = "benchmark",
            kpi_formula = "kpi_formula",
            value_cal_type = "value_cal_type",
            input_type = "input_type",
            is_apply_all = "is_apply_all",
            kpi_years = "kpi_years",
            is_kpi_not_weight = "is_kpi_not_weight",
            note = "note",
            lock = "lock",
            created_by="uc.login_account",
            created_on="created_on",
            modified_on="switch(case(modified_on!='',modified_on),'')",
            modified_by="switch(case(modified_by!='',um.login_account),'')"
            ).match("kpi_code == {0}", args['data']['kpi_code'])

        return ret.get_item()

    except Exception as ex:
        raise(ex)

def remove_job_working_kpi_by_kpi_code(args):
    try:
        ret = common.get_collection('HCSLS_JobWorking').update_many({
            "kpi":{
                "$elemMatch":{
                    "kpi_code":args['data']['kpi_code']
                    }
                }
            },
            {
                '$pull':{"kpi" :{ "kpi_code": args['data']['kpi_code']}}
            }
        )
        #if ret.raw_result['updatedExisting'] == True:
        ret.raw_result.update(error=None)
        return ret.raw_result
        #else:
        #    ret.raw_result.update(error="update error")
        #    return ret.raw_result
    except Exception as ex:
        raise(ex)

def get_kpi_by_kpi_code(args):
    try:
        collection = common.get_collection('TMLS_KPI')
        ret = collection.aggregate([
        {'$lookup': {
            'foreignField': 'value', 
            'as': 'val', 
            'from': common.get_collection_name_with_schema('SYS_VW_ValueList'),
            'localField': 'cycle_type'
            }
        }, 
        {'$unwind': {
            'path': '$val', 
            'preserveNullAndEmptyArrays': True
            }
        }, 
        {'$match': {   
            '$and':[{
                        '$or' :[{ 'val.list_name':None},
                                { 'val.list_name':'LCycleType'}]
                    },
                    {
                        '$or' :[{ 'val.language':None},
                                { 'val.language': common.get_language()}]
                    }]
            }
        },
        {'$lookup': {
            'foreignField': 'unit_code', 
            'as': 'unit', 
            'from': common.get_collection_name_with_schema('HCSLS_Unit'), 
            'localField': 'unit_code'
            }
        }, 
        {'$unwind': {
            'path': '$unit', 
            'preserveNullAndEmptyArrays': True
            }
        }, 
        {'$project': {
            'kpi_name': '$kpi_name', 
            'is_apply_all': '$is_apply_all', 
            'kpi_desc': '$kpi_desc', 
            'cycle_type': { '$ifNull': [ '$val.caption', '' ] }, 
            'kpi_code': { '$ifNull': [ '$kpi_code', '' ] }, 
            'weight': '$weight', 
            'unit_code': { '$ifNull': [ '$unit.unit_name', '' ] }, 
            'lock': '$lock', 
            'benchmark': { '$ifNull': [ '$benchmark', '' ] }
            }
        }, 
        {'$match': {'lock': {'$ne': True}, 'kpi_code':{'$eq':args['data']['kpi_code']}}}])

        return (lambda x: x[0] if x != None and len(x) > 0 else None)(list(ret))
    except Exception as ex:
        raise(ex)

def insert(args):
    try:
        lock.acquire()
        ret = {}
        if args['data'] != None:
            data =  set_dict_insert_data(args)
            ret  =  models.TMLS_KPI().insert(data)
            if args['data'].has_key('job_working') and len(args['data']['job_working']) > 0:
                insert_job_working_kpi(args['data']['job_working'], args['data'])
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
    try:
        lock.acquire()
        ret = {}
        if args['data'] != None:
            data =  set_dict_update_data(args)
            ret  =  models.TMLS_KPI().update(
                data, 
                "kpi_code == {0}", 
                args['data']['kpi_code'])
            if ret.has_key('error') and ret['error'] == None and ret['data'].raw_result['updatedExisting'] == True:
                if args['data'].has_key('job_working') and len(args['data']['job_working']) > 0:
                    insert_job_working_kpi(args['data']['job_working'], args['data'])
            if ret.has_key('error') and ret['error'] == None and ret['data'].raw_result['updatedExisting'] == True:
                ret.update(
                    item = KPI.display_list_kpi(args['data']['kpi_group_code']).match("kpi_code == {0}", args['data']['kpi_code']).get_item()
                    )
            lock.release()
            return ret

        lock.release()
        return dict(
            error = "request parameter is not exist"
        )
    except Exception as ex:
        lock.release()
        raise(ex)

def delete(args):
    try:
        lock.acquire()
        ret = {}
        if args['data'] != None:
            ret  =  models.TMLS_KPI().delete("kpi_code in {0}",[x["kpi_code"]for x in args['data']])
            lock.release()
            return ret

        lock.release()
        return dict(
            error = "request parameter is not exist"
        )
    except Exception as ex:
        lock.release()
        raise(ex)

def insert_job_working_kpi(job_w_code, kpi):
    try:
        if(len(job_w_code)) > 0:
            exist = models.HCSLS_VW_JobWorkingKPI().aggregate().project(
                rec_id = 1,
                kpi_code = 1,
                job_w_code = 1,
                job_w_name = 1,
                kpi_name = 1,
                unit = 1,
                description = 1,
                cycle = 1,
                weight = 1,
                standard_mark = 1,
                ordinal = 1,
                note = 1,
                created_on = 1,
                created_by = 1,
                modified_on = 1,
                modified_by = 1
                ).match("kpi_code == @kpi_code", kpi_code = kpi['kpi_code']).get_list()
            list_insert = []
            for x in job_w_code:
                if x not in map(lambda d: d['job_w_code'], exist):
                    list_insert.append({
                        "rec_id":common.generate_guid(),
                        "job_w_code": x,
                        "kpi_code":kpi.get('kpi_code', None),
                        "kpi_name":kpi.get('kpi_name', None),
                        "unit":kpi.get('unit_code', None),
                        "description":kpi.get('description', None),
                        "cycle":kpi.get('cycle', None),
                        "weight":kpi.get('weight', None),
                        "standard_mark":kpi.get('standard_mark', None),
                        "ordinal":kpi.get('ordinal', None),
                        "note":kpi.get('note', None),
                        "created_on":datetime.datetime.now(),
                        "created_by":common.get_user_id()
                        })
                else:
                    find = filter(lambda y: y['job_w_code'] == x, exist)[0]
                    list_insert.append(find)

            ret = {}
            for x in exist:
                ret = common.get_collection('HCSLS_JobWorking').update(
                        {
                            "job_w_code": x['job_w_code']
                        },
                        {
                            '$pull':{"kpi" :{ "rec_id": x['rec_id']}}
                        }, 
                        True
                        )

            if len(list_insert) > 0:
                for x in list_insert:
                    code = x['job_w_code']
                    del x['job_w_code']
                    ret = common.get_collection('HCSLS_JobWorking').update(
                        { "job_w_code": code },
                        {
                        '$push': {
                            "kpi": x
                            }
                        }
                        )

            return ret

    except Exception as ex:
        raise(ex)

def set_dict_insert_data(args):
    ret_dict = dict()

    ret_dict.update(
        kpi_code          = (lambda x: x['kpi_code']           if x.has_key('kpi_code')          else None)(args['data']),
        kpi_name          = (lambda x: x['kpi_name']           if x.has_key('kpi_name')          else None)(args['data']),
        kpi_name2         = (lambda x: x['kpi_name2']          if x.has_key('kpi_name2')         else None)(args['data']),
        kpi_group_code    = (lambda x: x['kpi_group_code']     if x.has_key('kpi_group_code')    else None)(args['data']),
        unit_code         = (lambda x: x['unit_code']          if x.has_key('unit_code')         else None)(args['data']),
        cycle_type        = (lambda x: x['cycle_type']         if x.has_key('cycle_type')        else None)(args['data']),
        kpi_desc          = (lambda x: x['kpi_desc']           if x.has_key('kpi_desc')          else None)(args['data']),
        kpi_ref           = (lambda x: x['kpi_ref']            if x.has_key('kpi_ref')           else None)(args['data']),
        weight            = (lambda x: x['weight']             if x.has_key('weight')            else None)(args['data']),
        benchmark         = (lambda x: x['benchmark']          if x.has_key('benchmark')         else None)(args['data']),
        kpi_formula       = (lambda x: x['kpi_formula']        if x.has_key('kpi_formula')       else None)(args['data']),
        value_cal_type    = (lambda x: x['value_cal_type']     if x.has_key('value_cal_type')    else None)(args['data']),
        input_type        = (lambda x: x['input_type']         if x.has_key('input_type')        else None)(args['data']),
        is_apply_all      = (lambda x: x['is_apply_all']       if x.has_key('is_apply_all')      else None)(args['data']),
        kpi_years         = (lambda x: x['kpi_years']          if x.has_key('kpi_years')         else None)(args['data']),
        is_kpi_not_weight = (lambda x: x['is_kpi_not_weight']  if x.has_key('is_kpi_not_weight') else None)(args['data']),
        note              = (lambda x: x['note']               if x.has_key('note')              else None)(args['data']),
        lock              = (lambda x: x['lock']               if x.has_key('lock')              else None)(args['data'])
    )

    return ret_dict

def set_dict_update_data(args):
    ret_dict = set_dict_insert_data(args)
    del ret_dict['kpi_code']
    return ret_dict