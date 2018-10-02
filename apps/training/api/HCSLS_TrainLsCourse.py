# -*- coding: utf-8 -*-
from bson import ObjectId
import models
import common
import datetime
from Query import TrainCourseGroup
from Query import TrainCourse
import logging
import threading
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

    if not args['data'].has_key('train_group_code') or args['data']['train_group_code'] == None or args['data']['train_group_code'] == "":
        return None

    ret=TrainCourse.display_list_train_ls_course(args['data']['train_group_code'])
    #ret = TrainCourse.display_list_train_ls_course()
    ret=common.filter_lock(ret, args)

    if (searchText != None):
        ret.match("contains(course_code, @name) or contains(course_name, @name)" + \
                  " or contains(course_content, @name) or contains(ordinal, @name)", name=searchText.strip())

    if(sort != None):
        ret.sort(sort)
        
    return ret.get_page(pageIndex, pageSize)

# def delete_factor_appraisal(args):
#     try:
#         lock.acquire()
#         ret = {}
#         rs = {
#             "deleted": 0,
#             "error":None
#             }
#         err = None
#         if args['data']['factor_code'] != None:
#             collection  =  common.get_collection('HCSLS_JobWorking')
#             try:
#                 for x in args['data']['job_w_code']:
#                     ret = collection.update(
#                     {
#                         "job_w_code": str(x).format(),
#                     },
#                     {
#                         "$pull":
#                             {
#                                 "factor_appraisal" : {
#                                     "factor_code": args['data']['factor_code']
#                                     }
#                             }
#                     },
#                     True)
#
#                     if ret['updatedExisting'] and ret['nModified'] > 0:
#                         rs['deleted'] += ret['nModified']
#
#                 lock.release()
#                 return rs
#             except Exception as ex:
#                 err = ex
#
#             lock.release()
#             return dict(
#                 error = (lambda x: err.message if x != None else None)(err),
#                 data = ret
#                 )
#
#         lock.release()
#         return dict(
#             error = "request parameter 'factor_code' is not exist"
#         )
#     except Exception as ex:
#         lock.release()
#         raise(ex)

# def get_factor_appraisal_by_factor_code(args):
#     try:
#         ret = models.HCSLS_VW_JobWorkingFactorAppraisal().aggregate().project(
#             job_w_code = 1,
#             factor_code = 1
#             ).match("factor_code == {0}", args['data']['factor_code'])
#         ret.project(
#             _id = 0,
#             job_w_code = 1
#             )
#         return ret.get_list()
#     except Exception as ex:
#         raise(ex)



def insert(args):
    try:
        lock.acquire()
        ret = {}
        if args['data'] != None:
            data =  set_dict_insert_data(args)
            ret  =  models.HCSLS_TrainLsCourse().insert(data)
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
            ret  =  models.HCSLS_TrainLsCourse().update(
                data, 
                "course_code == {0}",
                args['data']['course_code'])
            if ret['data'].raw_result['updatedExisting'] == True:
                ret.update(
                    item = TrainCourse.display_list_train_ls_course(args['data']['train_group_code']).match("course_code == {0}", args['data']['course_code']).get_item()
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
            ret  =  models.HCSLS_TrainLsCourse().delete("course_code in {0}",[x["course_code"]for x in args['data']])
            lock.release()
            return ret

        lock.release()
        return dict(
            error = "request parameter is not exist"
        )
    except Exception as ex:
        lock.release()
        raise(ex)

def set_dict_insert_data(args):
    ret_dict = dict()

    ret_dict.update(
        course_code         = (lambda x: x['course_code']        if x.has_key('course_code')       else None)(args['data']),
        course_name         = (lambda x: x['course_name']        if x.has_key('course_name')       else None)(args['data']),
        course_name2        = (lambda x: x['course_name2']       if x.has_key('course_name2')      else None)(args['data']),
        course_content      = (lambda x: x['course_content']     if x.has_key('course_content')    else None)(args['data']),
        train_group_code    = (lambda x: x['train_group_code']   if x.has_key('train_group_code')  else None)(args['data']),
        profession_code     = (lambda x: x['profession_code']    if x.has_key('profession_code')   else None)(args['data']),
        field_code          = (lambda x: x['field_code']         if x.has_key('field_code')        else None)(args['data']),
        method              = (lambda x: x['method']             if x.has_key('method')            else None)(args['data']),
        periodic            = (lambda x: x['periodic']           if x.has_key('periodic')          else None)(args['data']),
        number_month        = (lambda x: x['number_month']       if x.has_key('number_month')      else None)(args['data']),
        learner_min         = (lambda x: x['learner_min']        if x.has_key('learner_min')       else None)(args['data']),
        learner_max         = (lambda x: x['learner_max']        if x.has_key('learner_max')       else None)(args['data']),
        train_hours         = (lambda x: x['train_hours']        if x.has_key('train_hours')       else None)(args['data']),
        supplier_code       = (lambda x: x['supplier_code']      if x.has_key('supplier_code')     else None)(args['data']),
        room_code           = (lambda x: x['room_code']          if x.has_key('room_code')         else None)(args['data']),
        activity_task       = (lambda x: x['activity_task']      if x.has_key('activity_task')     else None)(args['data']),
        certificate_form    = (lambda x: x['certificate_form']   if x.has_key('certificate_form')  else None)(args['data']),
        after_month_work    = (lambda x: x['after_month_work']   if x.has_key('after_month_work')  else None)(args['data']),
        note                = (lambda x: x['note']               if x.has_key('note')              else None)(args['data']),
        ordinal             = (lambda x: x['ordinal']            if x.has_key('ordinal')           else None)(args['data']),
        lock                = (lambda x: x['lock']               if x.has_key('lock')              else None)(args['data'])
    )

    return ret_dict

def set_dict_update_data(args):
    ret_dict = set_dict_insert_data(args)
    del ret_dict['course_code']
    return ret_dict