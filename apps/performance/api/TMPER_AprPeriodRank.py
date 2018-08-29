# -*- coding: utf-8 -*-
from bson import ObjectId
import models
import common
import logging
import threading
logger = logging.getLogger(__name__)
global lock
lock = threading.Lock()
from bson import SON
import quicky

def get_tree(args):
    ret = {}
    collection = common.get_collection('TMPER_AprPeriodRank').aggregate([
        {"$lookup":{'from':('lv.HCSSYS_Departments'), 'localField':'department_code', 'foreignField':'department_code', 'as': 'dd'}},
        {"$unwind":{'path':'$dd', "preserveNullAndEmptyArrays":True}},
        {"$lookup":{'from':('lv.TMLS_Rank'), 'localField':'rank_code', 'foreignField':'rank_code', 'as': 'rr'}},
        {"$unwind":{'path':'$rr', "preserveNullAndEmptyArrays":True}},
        {"$match":{
            "$and": [ { 'apr_period': args['data']['apr_period'] }, { 'apr_year': args['data']['apr_year']} ]
        }},
        {"$project": {
            "apr_period":1,
            "apr_year":1,
            "department_code": 1,
            "department_name":{ "$ifNull": ["$dd.department_name", ""] },
            "rank_code":1,
            "rank_name": { "$ifNull": ["$rr.rank_name", ""] },
            "percent":1,
            "level" : { "$ifNull": ["$dd.level", ""] },
            "level_code" : { "$ifNull": ["$dd.level_code", ""] },
            "ordinal": { "$ifNull": ["$dd.ordinal", ""] },
            "parent_code":{ "$ifNull": ["$dd.parent_code", ""] },
            "note":1
        }},
        { "$sort" : SON([("ordinal",1),("rank_name",1)]) }
        ])
        
    ret = list(collection)
    return ret

def get_genPreAperiodData(args):
    if(args['data']!= None):
        ret = {}
        collection = common.get_collection('TMPER_AprPeriodRank').aggregate([
        {"$match":{
            "$and": [ { 'apr_year': int(args['data']['apr_year']) }, { 'apr_period': int(args['data']['apr_period'])} ]
        }},
        {"$project": {
            "apr_period":1,
            "apr_year": 1,
            "department_code": 1,
            "rank_code":1,
            "percent":1,
            "note":1
        }},
        #{ "$sort" : SON([("apr_year",-1),("apr_period",-1)]) }
        ])
        ret = list(collection)
        return ret


def generate(args):
    try:
        lock.acquire()
        ret = {}
        listRankPerNow = get_RankDataByPeriodAndYear(args)
        if(len(listRankPerNow) > 0 and len(args['data']['res']) >0):
            if args['data'] != None and args['data'].has_key('now_apr_period') and args['data'].has_key('now_apr_year') :
                if(args['data'].has_key('chk_exchangeData') and args['data']['chk_exchangeData'] == 1):
                    ret  =  models.TMPER_AprPeriodRank().delete("_id in {0}",[ObjectId(x["_id"]) for x in listRankPerNow])
                    for item in args['data']['res']:
                        item['apr_period'] = args['data']['now_apr_period']
                        item['apr_year'] =  args['data']['now_apr_year']
                        data = set_dict_insert_data(item)
                        ret  =  models.TMPER_AprPeriodRank().insert(data)
                else:
                    for  item in args['data']['res'] :
                        if item.has_key('apr_period' and 'apr_year' and 'department_code'):
                            for index, rank in enumerate(listRankPerNow, start=0):
                                if (item['department_code'] == rank['department_code']):
                                     if(rank['department_code'] == None or rank['department_code'] == ""):
                                         rank['department_code'] = item['department_code']
                                     if(rank['rank_code'] == None or rank['rank_code'] == ""):
                                         rank['rank_code'] = item['rank_code']
                                     if(rank['percent'] == None or rank['percent'] == ""):
                                         rank['percent'] = item['percent']
                                     if(rank['note'] == None or rank['note'] == ""):
                                         rank['note'] = item['note']
                                     data = set_dict_update_data(rank)
                                     ret  =  models.TMPER_AprPeriodRank().update(
                                                 data, 
                                                "_id == {0}", 
                                                 ObjectId(rank['_id']))
                                     break
                                else:
                                    if(index == len(listRankPerNow)-1):
                                        item['apr_period'] = args['data']['now_apr_period']
                                        item['apr_year'] =  args['data']['now_apr_year']
                                        data =  set_dict_insert_data(item)
                                        ret  =  models.TMPER_AprPeriodRank().insert(data)
                                    else:
                                        continue
                lock.release()
                return ret
        elif(len(listRankPerNow) == 0 and len(args['data']['res']) >0):
            for item in args['data']['res']:
                item['apr_period'] = args['data']['now_apr_period']
                item['apr_year'] =  args['data']['now_apr_year']
                data = set_dict_insert_data(item)
                ret  =  models.TMPER_AprPeriodRank().insert(data)
            lock.release()
            return ret
        lock.release()
        return dict(
            error = "request parameter is not exist"
            )
    except Exception as ex:
        lock.release()
        raise(ex)

def get_RankDataByPeriodAndYear(args):
    if(args['data']!= None):
        ret = {}
        collection = common.get_collection('TMPER_AprPeriodRank').aggregate([
        {"$match":{
            "$and": [ { 'apr_year': args['data']['now_apr_year'] }, { 'apr_period': args['data']['now_apr_period']} ]
        }},
        {"$project": {
            "apr_period":1,
            "apr_year": 1,
            "department_code": 1,
            "rank_code":1,
            "percent":1,
            "note":1
        }},
        #{ "$sort" : SON([("apr_year",-1),("apr_period",-1)]) }
        ])
        ret = list(collection)
        return ret

def insert(args):
    try:
        lock.acquire()
        ret = {}
        if args['data'] != None:
            data =  set_dict_insert_data(args)
            ret  =  models.TMPER_AprPeriodRank().insert(data)
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
            ret  =  models.TMPER_AprPeriodRank().update(
                data, 
                "_id == {0}", 
                ObjectId(args['data']['_id']))
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
            args['data'].pop(0)
            ret  =  models.TMPER_AprPeriodRank().delete("_id in {0}",[ObjectId(x["_id"])for x in args['data']])
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
        department_code        = (lambda x: x['department_code']       if x.has_key('department_code')      else None)(item),
        rank_code   = (lambda x: x['rank_code']  if x.has_key('rank_code') else None)(item),
        percent              = (lambda x: x['percent']             if x.has_key('percent')            else None)(item),
        note                = (lambda x: x['note']               if x.has_key('note')              else None)(item)
    )

    return ret_dict

def set_dict_update_data(args):
    ret_dict = set_dict_insert_data(args)
    return ret_dict