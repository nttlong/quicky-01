# -*- coding: utf-8 -*-
from bson import ObjectId
import models
import common
from Query import AprPeriod, AprPeriodEmpOut, AprPeriodRank
from hcs_authorization import action_type,authorization
import logging
import threading
logger = logging.getLogger(__name__)
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

    ret=AprPeriod.display_list_apr_period(searchText)
    ret=common.filter_lock(ret, args)
    if(sort != None):
        ret.sort(sort)
      
    return ret.get_page(pageIndex, pageSize)

@authorization.authorise(action=action_type.Action.READ)
def get_item_by_period_year(args):
    ret=models.TMPER_AprPeriod().aggregate()
    ret.left_join(models.auth_user_info(), "created_by", "username", "uc")
    ret.left_join(models.auth_user_info(), "modified_by", "username", "um")
    ret.project(
        _id=1,
        apr_period="apr_period",
        apr_year="apr_year",
        give_target_from="give_target_from",
        give_target_to="give_target_to",
        review_mid_from="review_mid_from",
        review_mid_to="review_mid_to",
        approval_mid_from="approval_mid_from",
        approval_mid_to="approval_mid_to",
        emp_final_from="emp_final_from",
        emp_final_to="emp_final_to",
        approval_final_from="approval_final_from",
        approval_final_to="approval_final_to",
        note="note",
        created_by="uc.login_account",
        created_on="created_on",
        modified_on="switch(case(modified_on!='',modified_on),'')",
        modified_by="switch(case(modified_by!='',um.login_account),'')",
    )
    
    ret.match("apr_period == {0} and apr_year == {1}", args['data']['apr_period'], args['data']['apr_year'])
    ret.sort(dict(
        apr_year =1,
    ))

    return ret.get_item()


@authorization.authorise(action=action_type.Action.WRITE)
def save(args):
    try:
        lock.acquire()
        ret = {}
        if args['data'] != None:
            item = get_item_by_period_year(args)
            if item!= None:
                data = set_dict_update_data(args)
                ret = models.TMPER_AprPeriod().update(
                    data,
                    "_id == {0}",
                    ObjectId(item['_id']))
            else:
                data =  set_dict_insert_data(args)
                ret  =  models.TMPER_AprPeriod().insert(data)
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
            for item in args['data']:
                list_emp_out = AprPeriodEmpOut.get_apr_emp_out_by_apr_period_year(item['apr_period'], item['apr_year'])
                list_rank = AprPeriodRank.get_apr_rank_by_apr_period_year(item['apr_period'], item['apr_year'])
                if(len(list_emp_out) > 0):
                    models.TMPER_AprPeriodEmpOut().delete("_id in {0}",
                                            [ObjectId(item_emp_out["_id"]) for item_emp_out in list_emp_out])
                if(len(list_rank) > 0):
                    models.TMPER_AprPeriodRank().delete("_id in {0}",
                                                      [ObjectId(item_rank["_id"]) for item_rank in list_rank])
                ret = models.TMPER_AprPeriod().delete("_id in {0}", [ObjectId(item["_id"])])
            lock.release()
            return ret

        lock.release()
        return dict(
            error = "request parameter is not exist"
        )
    except Exception as ex:
        lock.release()
        raise(ex)

@authorization.authorise(common= True)
def set_dict_insert_data(args):
    ret_dict = dict()
    ret_dict.update(
        apr_period      =                   (lambda x: x['apr_period']      if x.has_key('apr_period')       else None)(args['data']),
        apr_year      =                     (lambda x: x['apr_year']      if x.has_key('apr_year')       else None)(args['data']),
        give_target_from     =              (lambda x: x['give_target_from']     if x.has_key('give_target_from')      else None)(args['data']),
        give_target_to            =         (lambda x: x['give_target_to']            if x.has_key('give_target_to')             else None)(args['data']),
        review_mid_from               =     (lambda x: x['review_mid_from']               if x.has_key('review_mid_from')                else None)(args['data']),
        review_mid_to               =       (lambda x: x['review_mid_to']               if x.has_key('review_mid_to')                else None)(args['data']),
        approval_mid_from     =                (lambda x: x['approval_mid_from']     if x.has_key('approval_mid_from')      else None)(args['data']),
        approval_mid_to            =           (lambda x: x['approval_mid_to']            if x.has_key('approval_mid_to')             else None)(args['data']),
        emp_final_from               = (lambda x: x['emp_final_from']               if x.has_key('emp_final_from')                else None)(args['data']),
        emp_final_to               =   (lambda x: x['emp_final_to']               if x.has_key('emp_final_to')                else None)(args['data']),
        approval_final_from               = (lambda x: x['approval_final_from']               if x.has_key('approval_final_from')                else None)(args['data']),
        approval_final_to               =   (lambda x: x['approval_final_to']               if x.has_key('approval_final_to')                else None)(args['data']),
        note                      =   (lambda x: x['note']               if x.has_key('note')                else None)(args['data'])
        )

    return ret_dict

@authorization.authorise(common= True)
def set_dict_update_data(args):
    ret_dict = set_dict_insert_data(args)
    #del ret_dict['_id']
    return ret_dict

