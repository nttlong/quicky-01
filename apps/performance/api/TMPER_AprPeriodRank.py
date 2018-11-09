# -*- coding: utf-8 -*-
from bson import ObjectId
import qmongo
import models
import common
import logging
import threading
from hcs_authorization import action_type,authorization
from Query import TMLS_Rank
from services import TMPER_AprPeriodRankService as service
logger = logging.getLogger(__name__)
global lock
import quicky
lock = threading.Lock()
from Query import AprPeriodRank
from bson import SON
#from qmongo import qcollections
@authorization.authorise(action=action_type.Action.READ)
def get_tree(args):
    ret = {}
    collection = common.get_collection('TMPER_AprPeriodRank').aggregate([
        {"$lookup": {'from': ('lv.HCSSYS_Departments'), 'localField': 'department_code',
                     'foreignField': 'department_code', 'as': 'dd'}},
        {"$unwind": {'path': '$dd', "preserveNullAndEmptyArrays": True}},
        {"$lookup": {'from': ('lv.TMLS_Rank'), 'localField': 'rank_code', 'foreignField': 'rank_code', 'as': 'rr'}},
        {"$unwind": {'path': '$rr', "preserveNullAndEmptyArrays": True}},
        {"$match": {
            "$and": [{'apr_period': args['data']['apr_period']}, {'apr_year': args['data']['apr_year']}]
        }},
        {"$project": {
            "apr_period": 1,
            "apr_year": 1,
            "department_code": 1,
            "department_name": {"$ifNull": ["$dd.department_name", ""]},
            "rank_name": {"$ifNull": ["$rr.rank_name", ""]},
            "level": {"$ifNull": ["$dd.level", ""]},
            "level_code": {"$ifNull": ["$dd.level_code", ""]},
            "ordinal": {"$ifNull": ["$dd.ordinal", ""]},
            "parent_code": {"$ifNull": ["$dd.parent_code", ""]},
            "note": 1,
            "rank_level": 1
        }},
        {"$sort": SON([("ordinal", 1), ("rank_name", 1)])}
    ])
    ret = list(collection)
    if (ret != None):
        list_rank_code = TMLS_Rank.getListRank(args)
        for idx, val in enumerate(ret):
            if (val['rank_level'] != None):
                for index, value in enumerate(list_rank_code):
                    val[val['rank_level'][index]['rank_code']] = val['rank_level'][index]['percent']
    return ret
@authorization.authorise(action=action_type.Action.READ)
def get_genPreAperiodData(args):
    if (args['data'] != None):
        ret = {}
        collection = common.get_collection('TMPER_AprPeriodRank').aggregate([
            {"$match": {
                "$and": [{'apr_year': int(args['data']['apr_year'])}, {'apr_period': int(args['data']['apr_period'])}]
            }},
            {"$project": {
                "apr_period": 1,
                "apr_year": 1,
                "department_code": 1,
                "rank_level": 1,
                "note": 1
            }},
            # { "$sort" : SON([("apr_year",-1),("apr_period",-1)]) }
        ])
        ret = list(collection)
        return ret
@authorization.authorise(action=action_type.Action.CREATE)
def generate(args):
    try:
        lock.acquire()
        ret = {}
        listRankPerNow = get_RankDataByPeriodAndYear(args)
        if (len(listRankPerNow) > 0 and len(args['data']['res']) > 0):
            if args['data'] != None and args['data'].has_key('now_apr_period') and args['data'].has_key('now_apr_year'):
                if (args['data'].has_key('chk_exchangeData') and args['data']['chk_exchangeData'] == 1):
                    ret = qmongo.models.TMPER_AprPeriodRank.delete("_id in {0}",
                                                              [ObjectId(x["_id"]) for x in listRankPerNow])
                    for item in args['data']['res']:
                        item['apr_period'] = args['data']['now_apr_period']
                        item['apr_year'] = args['data']['now_apr_year']
                        data = set_dict_insert_data(item)
                        ret = qmongo.models.TMPER_AprPeriodRank.insert(data)
                else:
                    for item in args['data']['res']:
                        if item.has_key('apr_period' and 'apr_year' and 'department_code'):
                            for index, rank in enumerate(listRankPerNow, start=0):
                                if (item['department_code'] == rank['department_code']):
                                    rank['rank_level'] = item['rank_level']
                                    if (rank['note'] == None or rank['note'] == ""):
                                        rank['note'] = item['note']
                                    data = set_dict_update_data(rank)
                                    ret = qmongo.models.TMPER_AprPeriodRank.update(
                                        data,
                                        "_id == {0}",
                                        ObjectId(rank['_id']))
                                    break
                                else:
                                    if (index == len(listRankPerNow) - 1):
                                        item['apr_period'] = args['data']['now_apr_period']
                                        item['apr_year'] = args['data']['now_apr_year']
                                        data = set_dict_insert_data(item)
                                        ret = qmongo.models.TMPER_AprPeriodRank.insert(data)
                                    else:
                                        continue
                lock.release()
                return ret
        elif (len(listRankPerNow) == 0 and len(args['data']['res']) > 0):
            for item in args['data']['res']:
                item['apr_period'] = args['data']['now_apr_period']
                item['apr_year'] = args['data']['now_apr_year']
                data = set_dict_insert_data(item)
                ret = qmongo.models.TMPER_AprPeriodRank.insert(data)
            lock.release()
            return ret
        lock.release()
        return dict(
            error="request parameter is not exist"
        )
    except Exception as ex:
        lock.release()
        raise (ex)
@authorization.authorise(action=action_type.Action.READ)
def get_RankDataByPeriodAndYear(args):
    if (args['data'] != None):
        ret = {}
        collection = common.get_collection('TMPER_AprPeriodRank').aggregate([
            {"$match": {
                "$and": [{'apr_year': args['data']['now_apr_year']}, {'apr_period': args['data']['now_apr_period']}]
            }},
            {"$project": {
                "apr_period": 1,
                "apr_year": 1,
                "department_code": 1,
                "rank_level": 1,
                "note": 1
            }},
            # { "$sort" : SON([("apr_year",-1),("apr_period",-1)]) }
        ])
        ret = list(collection)
        return ret
@authorization.authorise(action=action_type.Action.READ)
def get_parent_code_by_departCode(args):
    if (args != None):
        ret = []
        used = []
        qr = qcollections.queryable(common.get_collection("HCSSYS_Departments")).items
        for i in args:
            for x in qr:
                if (i == x['department_code']):
                    ret.append(x['parent_code'])
                    break
        unique = list(set(ret))
        return unique
@authorization.authorise(action=action_type.Action.CREATE)
def insert(args):
    try:
        lock.acquire()
        ret = {}
        if args['data'] != None and args['data'].has_key(
                'list_rating' and 'departments' and 'apr_period' and 'apr_year'):
            if (len(args['data']['list_rating']) > 0 and len(args['data']['departments']['department_code']) > 0):
                tmp_depart = []
                dbs = service.get_all_department_by_year_month(args['data'])
                if (len(dbs) > 0):
                    for x in dbs:
                        tmp_depart.append(x['department_code'])
                for dep_code in args['data']['departments']['department_code']:
                    if (len(tmp_depart) > 0 and tmp_depart.__contains__(dep_code)):
                        for x in dbs:
                            if (x['department_code'] == dep_code):
                                # update department and list rating
                                ite = {}
                                x['apr_period'] = args['data']['apr_period']
                                x['apr_year'] = args['data']['apr_year']
                                x['department_code'] = dep_code
                                if args['data']['departments'].has_key('note'):
                                    x['note'] = args['data']['departments']['note']
                                else:
                                    x['note'] = ""
                                ite['rank_level'] = []
                                for item in args['data']['list_rating']:
                                    tmp = {}
                                    tmp['rank_code'] = item['rank_code']
                                    if (item['percent'] == "0"):
                                        tmp['percent'] = 0
                                    else:
                                        tmp['percent'] = item['percent']
                                    ite['rank_level'].append(tmp)
                                x['rank_level'] = ite['rank_level']
                                data = set_dict_update_data(x)
                                ret = qmongo.models.TMPER_AprPeriodRank.update(
                                    data,
                                    "_id == {0}",
                                    ObjectId(x['_id']))
                    else:
                        # insert department and list rating
                        ite = {}
                        ite['apr_period'] = args['data']['apr_period']
                        ite['apr_year'] = args['data']['apr_year']
                        ite['department_code'] = dep_code
                        if args['data']['departments'].has_key('note'):
                            ite['note'] = args['data']['departments']['note']
                        else:
                            ite['note'] = ""
                        ite['rank_level'] = []
                        for item in args['data']['list_rating']:
                            tmp = {}
                            tmp['rank_code'] = item['rank_code']
                            if (item['percent'] == "0"):
                                tmp['percent'] = 0
                            else:
                                tmp['percent'] = item['percent']
                            ite['rank_level'].append(tmp)
                        data = set_dict_insert_data(ite)
                        ret = qmongo.models.TMPER_AprPeriodRank.insert(data)
                # get parent_code from department in Department,
                arr = args['data']['departments']['department_code']
                while (all(y is None for y in arr) == False):
                    arr_calback = service.get_parent_code_by_departCode(arr)
                    for dep_code in arr_calback:
                        if dep_code is None:
                            continue
                        elif (dep_code in arr) or (dep_code in tmp_depart):
                            arr_calback.remove(dep_code)
                        else:
                            ite = {}
                            ite['apr_period'] = args['data']['apr_period']
                            ite['apr_year'] = args['data']['apr_year']
                            ite['department_code'] = dep_code
                            ite['rank_level'] = None
                            data = set_dict_insert_data(ite)
                            ret = qmongo.models.TMPER_AprPeriodRank.insert(data)
                    arr = arr_calback
                lock.release()
                return ret
        lock.release()
        return dict(
            error="request parameter is not exist"
        )
    except Exception as ex:
        lock.release()
        raise (ex)
@authorization.authorise(action=action_type.Action.WRITE)
def update(args):
    try:
        lock.acquire()
        ret = {}
        if args['data'] != None and args['data'].has_key(
                'list_rating' and 'departments' and 'apr_period' and 'apr_year'):
            if (len(args['data']['list_rating']) > 0 and len(args['data']['departments']['department_code']) > 0):
                x = service.get_aprAprRank_by_departCode(args['data'])
                if (x != None):
                    ite = {}
                    ite['rank_level'] = []
                    for item in args['data']['list_rating']:
                        tmp = {}
                        tmp['rank_code'] = item['rank_code']
                        if (item['percent'] == "0"):
                            tmp['percent'] = 0
                        else:
                            tmp['percent'] = item['percent']
                        ite['rank_level'].append(tmp)
                    x['rank_level'] = ite['rank_level']
                    if args['data']['departments'].has_key('note'):
                        x['note'] = args['data']['departments']['note']
                    else:
                        x['note'] = ""
                    data = set_dict_update_data(x)
                    ret = qmongo.models.TMPER_AprPeriodRank.update(
                        data,
                        "_id == {0}",
                        ObjectId(x['_id']))
                lock.release()
                return ret
            lock.release()
            return dict(
                error="request parameter is not exist"
            )
    except Exception as ex:
        lock.release()
        raise (ex)
@authorization.authorise(action=action_type.Action.DELETE)
def delete(args):
    try:
        lock.acquire()
        ret = {}
        if args['data']!= None:
            for item in args['data']:
                if (item['level'] == 1 and item['parent_code'] == None):
                    _id = get_id_by_departCode(item)
                    item['_id'] = unicode(_id['_id'])
            ret = qmongo.models.TMPER_AprPeriodRank.delete("_id in {0}", [ObjectId(x["_id"]) for x in args['data']])
            lock.release()
            return ret
        lock.release()
        return dict(
            error="request parameter is not exist"
        )
    except Exception as ex:
        lock.release()
        raise (ex)
@authorization.authorise(common= True)
def set_dict_insert_data(item):
    ret_dict = dict()
    ret_dict.update(
        apr_period=(lambda x: x['apr_period'] if x.has_key('apr_period') else None)(item),
        apr_year=(lambda x: x['apr_year'] if x.has_key('apr_year') else None)(item),
        department_code=(lambda x: x['department_code'] if x.has_key('department_code') else None)(item),
        rank_level=(lambda x: x['rank_level'] if x.has_key('rank_level') else [])(item),
        note=(lambda x: x['note'] if x.has_key('note') else None)(item)
    )
    return ret_dict
@authorization.authorise(common= True)
def set_dict_update_data(args):
    ret_dict = set_dict_insert_data(args)
    return ret_dict
@authorization.authorise(action=action_type.Action.READ)
def get_all_department_by_year_month(args):
    ret = {}
    collection = common.get_collection('TMPER_AprPeriodRank').aggregate([
        {"$match": {
            "$and": [{'apr_period': args['apr_period']}, {'apr_year': args['apr_year']}]
        }},
        {"$project": {
            "_id": 1,
            "apr_period": 1,
            "apr_year": 1,
            "department_code": 1,
            "rank_level": 1,
            "note": 1
        }},
    ])
    ret = list(collection)
    return ret
@authorization.authorise(action=action_type.Action.READ)
def get_id_by_departCode(args):
    ret = {}
    collection = common.get_collection('TMPER_AprPeriodRank').aggregate([
        {"$match": {
            "$and": [{'apr_period': args['apr_period']}, {'apr_year': args['apr_year']},
                     {'department_code': args['department_code']}]
        }},
        {"$project": {
            "_id": 1,
        }},
    ])
    ret = list(collection)
    return (lambda x: x[0] if len(x) > 0 else None)(ret)
@authorization.authorise(action=action_type.Action.READ)
def get_aprAprRank_by_departCode(args):
    ret = {}
    collection = common.get_collection('TMPER_AprPeriodRank').aggregate([
        {"$match": {
            "$and": [{'apr_period': args['apr_period']}, {'apr_year': args['apr_year']},
                     {'department_code': args['departments']['department_code'][0]}]
        }},
        {"$project": {
            "_id": 1,
            "apr_period": 1,
            "apr_year": 1,
            "department_code": 1,
            "rank_level": 1,
            "note": 1
        }},
    ])
    ret = list(collection)
    return (lambda x: x[0] if len(x) > 0 else None)(ret)
@authorization.authorise(action=action_type.Action.READ)
def getListRankcodeWithData(args):
    ret = qmongo.models.TMPER_AprPeriodRank.aggregate
    ret.left_join(qmongo.models.auth_user_info, "created_by", "username", "uc")
    ret.left_join(qmongo.models.auth_user_info, "modified_by", "username", "um")
    ret.match("apr_period == {0} and apr_year == {1} and department_code == {2}",
              args['data']['apr_period'], args['data']['apr_year'], args['data']['department_code'])
    ret.project(
        rank_level=1,
        note=1,
        created_by="uc.login_account",
        created_on="created_on",
        modified_on="switch(case(modified_on!='',modified_on),'')",
        modified_by="switch(case(modified_by!='',um.login_account),'')",
    )
    ret = ret.get_item()
    if (ret != None):
        list_rank_code = TMLS_Rank.getListRank(args)
        for item in ret['rank_level']:
            if item['percent'] == 0:
                item['percent'] = '0'
            for i in list_rank_code:
                if (item['rank_code'] == i['rank_code']):
                    item['rank_name'] = i['rank_name']
                    break
    return ret
    return ret.get_item()
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
                collection1 = common.get_collection('TMPER_AprPeriodRank').aggregate([
                    {"$match": {
                        "$and": [{'apr_year': x['apr_year']}, {'apr_period': x['apr_period']}]
                    }},
                ])
                if (len(list(collection1)) == 0):
                    ret1.append(x)
        item_list = [e for e in ret if e not in ret1]
        return item_list