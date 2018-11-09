# -*- coding: utf-8 -*-
from bson import ObjectId
import qmongo
import models
from Query import KPI
import logging
import datetime
import threading
import common
from services import TMLS_CompetencyService as service
from hcs_authorization import action_type,authorization
logger = logging.getLogger(__name__)
from views.views import SYS_VW_ValueList;
#from views.views import HCSLS_VW_JobWorkingCompetency;
global lock
lock = threading.Lock()

@authorization.authorise(action=action_type.Action.READ)
def get_list_with_searchtext(args):
    searchText = args['data'].get('search', '')
    pageSize = args['data'].get('pageSize', 0)
    pageIndex = args['data'].get('pageIndex', 20)
    sort = args['data'].get('sort', 20)

    pageIndex = (lambda pIndex: pIndex if pIndex != None else 0)(pageIndex)
    pageSize = (lambda pSize: pSize if pSize != None else 20)(pageSize)

    collection = common.get_collection('TMLS_Competency')
    ret = collection.aggregate([
    {'$lookup': {
        'foreignField': 'value', 
        'as': 'val_aft', 
        'from': common.get_collection_name_with_schema('SYS_VW_ValueList'),
        'localField': 'apr_form_type'
        }
    }, 
    {'$unwind': {
        'path': '$val_aft', 
        'preserveNullAndEmptyArrays': True
        }
    }, 
    {'$match': {   
        '$and':[{
                    '$or' :[{ 'val_aft.list_name':None},
                            { 'val_aft.list_name':'PERF_AproveFormType'}]
                },
                {
                    '$or' :[{ 'val_aft.language':None},
                            { 'val_aft.language': common.get_language()}]
                }]
        }
    },
    {'$lookup': {
        'foreignField': 'value', 
        'as': 'val_pst', 
        'from':SYS_VW_ValueList().get_collection_name(),
        'localField': 'point_scale_type'
        }
    }, 
    {'$unwind': {
        'path': '$val_pst', 
        'preserveNullAndEmptyArrays': True
        }
    }, 
    {'$match': {   
        '$and':[{
                    '$or' :[{ 'val_pst.list_name':None},
                            { 'val_pst.list_name':'PERF_PointScaleType'}]
                },
                {
                    '$or' :[{ 'val_pst.language':None},
                            { 'val_pst.language': common.get_language()}]
                }]
        }
    },
    {'$lookup': {
        'foreignField': 'com_group_code', 
        'as': 'group', 
        'from': common.get_collection_name_with_schema('TMLS_CompetencyGroup'),
        'localField': 'com_group_code'
        }
    }, 
    {'$unwind': {
        'path': '$group', 
        'preserveNullAndEmptyArrays': True
        }
    }, 
    {'$project': {
        'com_code': '$com_code',
        'level_code': '$group.level_code',
        'com_group_code': '$com_group_code',
        'com_name': '$com_name',
        'com_type':'$com_type',
        'apr_form_type': { '$ifNull': [ '$val_aft.caption', '' ] },
        'point_scale_type': { '$ifNull': [ '$val_pst.caption', '' ] },
        'ordinal': '$ordinal', 
        'lock': '$lock'
        }
    }, 
    {'$match': {
        'lock': common.aggregate_filter_lock(args['data']['lock']), 
        'level_code':{'$eq':args['data']['com_group_code']},
        '$or': [(lambda x: {} if x == 0 else { "com_type" : x } )(args['data']['com_type'])]}
    }, 
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

@authorization.authorise(action=action_type.Action.READ)
def get_by_com_code(args):
    import qmongo
    try:
        ret =qmongo.models.TMLS_Competency.aggregate
        ret.lookup(qmongo.views.HCSLS_VW_JobWorkingCompetency, "com_code", "com_code", "comp")
        ret.left_join(qmongo.models.auth_user_info, "created_by", "username", "uc")
        ret.left_join(qmongo.models.auth_user_info, "modified_by", "username", "um")
        ret.project(
            job_working = "comp.job_w_code",
            com_code = "com_code",
            com_name = "com_name",
            com_name2 = "com_name2",
            com_group_code = "com_group_code",
            com_type = "com_type",
            apr_form_type = "apr_form_type",
            point_scale_type = "point_scale_type",
            score_from = "score_from",
            score_to = "score_to",
            bu_codes = "bu_codes",
            com_desc = "com_desc",
            note = "note",
            ordinal = "ordinal",
            lock = "lock",
            created_by="uc.login_account",
            created_on="created_on",
            modified_on="switch(case(modified_on!='',modified_on),'')",
            modified_by="switch(case(modified_by!='',um.login_account),'')"
            ).match("com_code == {0}", args['data']['competency'])

        return ret.get_item()

    except Exception as ex:
        raise(ex)

@authorization.authorise(action=action_type.Action.CREATE)
def insert(args):
    try:
        lock.acquire()
        ret = {}
        if args['data'] != None:
            data =  set_dict_insert_data(args['data'])
            ret  = qmongo.models.TMLS_Competency.insert(data)
            if args['data'].has_key('job_working') and len(args['data']['job_working']) > 0:
                service.insert_job_working_competency(args['data']['job_working'], args['data'])
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
            data =  set_dict_update_data(args['data'])
            ret  = qmongo.models.TMLS_Competency.update(
                data, 
                "com_code == {0}", 
                args['data']['com_code'])
            if ret.has_key('error') and ret['error'] == None and ret['data'].raw_result['updatedExisting'] == True:
                if args['data'].has_key('job_working') and len(args['data']['job_working']) > 0:
                    service.insert_job_working_competency(args['data']['job_working'], args['data'])
            if ret.has_key('error') and ret['error'] == None and ret['data'].raw_result['updatedExisting'] == True:
                ret.update(
                    item = args['data']
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

@authorization.authorise(action=action_type.Action.DELETE)
def delete(args):
    try:
        lock.acquire()
        ret = {}
        if args['data'] != None:
            ret  = qmongo.models.TMLS_Competency.delete("com_code in {0}",[x["com_code"]for x in args['data']])
            #delete level, delete action, delete factor
            qmongo.models.TMLS_CompetencyLevel.delete("com_code in {0}", [x["com_code"] for x in args['data']])
            qmongo.models.TMLS_CompetencyAction.delete("com_code in {0}", [x["com_code"] for x in args['data']])
            qmongo.models.TMLS_CompetencyFactor.delete("com_code in {0}", [x["com_code"] for x in args['data']])
            common.get_collection('HCSLS_JobWorking').update_many(
                {
                    "competency":{
                            "$elemMatch":{
                                "com_code": {"$in":[x["com_code"] for x in args['data']]}
                                }
                            }
                },
                {
                    "$pull": {"competency": { "com_code" : {"$in":[x["com_code"] for x in args['data']]}}}
                }
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

def insert_job_working_competency(job_w_code, comp):
    import qmongo
    try:
        if(len(job_w_code)) > 0:
            exist = qmongo.views.HCSLS_VW_JobWorkingCompetency.aggregate.project(
                rec_id = 1,
                job_w_code = 1,
                grade = 1,
                com_code = 1,
                com_level_code = 1,
                weight = 1,
                ordinal = 1,
                note = 1,
                created_on = 1,
                created_by = 1,
                modified_on = 1,
                modified_by = 1
                ).match("com_code == @com_code", com_code = comp['com_code']).get_list()
            list_insert = []
            for x in job_w_code:
                if x not in map(lambda d: d['job_w_code'], exist):
                    list_insert.append({
                        "rec_id": common.generate_guid(),
                        "job_w_code": x,
                        "grade": comp.get("grade", None),
                        "com_code": comp.get("com_code", None),
                        "com_level_code": comp.get("com_level_code", None),
                        "weight": comp.get("weight", None),
                        "ordinal": comp.get("ordinal", None),
                        "note": comp.get("note", None),
                        "created_on": datetime.datetime.now(),
                        "created_by": common.get_user_id()
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
                            '$pull':{"competency" :{ "rec_id": x['rec_id']}}
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
                            "competency": x
                            }
                        }
                        )

            return ret

    except Exception as ex:
        raise(ex)

@authorization.authorise(common= True)
def set_dict_insert_data(args):
    result = dict()
    result.update(
        com_code          = (lambda x: x['com_code']         if x.has_key('com_code')           else None)(args),
        com_name          = (lambda x: x['com_name']         if x.has_key('com_name')           else None)(args),
        com_name2         = (lambda x: x['com_name2']        if x.has_key('com_name2')          else None)(args),
        com_group_code    = (lambda x: x['com_group_code']   if x.has_key('com_group_code')     else None)(args),
        com_type          = (lambda x: x['com_type']         if x.has_key('com_type')           else None)(args),
        apr_form_type     = (lambda x: x['apr_form_type']    if x.has_key('apr_form_type')      else None)(args),
        point_scale_type  = (lambda x: x['point_scale_type'] if x.has_key('point_scale_type')   else None)(args),
        score_from        = (lambda x: x['score_from']       if x.has_key('score_from')         else None)(args),
        score_to          = (lambda x: x['score_to']         if x.has_key('score_to')           else None)(args),
        bu_codes          = (lambda x: x['bu_codes']         if x.has_key('bu_codes')           else None)(args),
        com_desc          = (lambda x: x['com_desc']         if x.has_key('com_desc')           else None)(args),
        note              = (lambda x: x['note']             if x.has_key('note')               else None)(args),
        ordinal           = (lambda x: x['ordinal']          if x.has_key('ordinal')            else None)(args),
        lock              = (lambda x: x['lock']             if x.has_key('lock')               else False)(args)
        )

    return result

@authorization.authorise(common= True)
def set_dict_update_data(args):
    result = set_dict_insert_data(args)
    del result['com_code']
    return result