# -*- coding: utf-8 -*-
from bson import ObjectId
import models
from Query import TrainCourseGroup
import logging
import threading
import common
logger = logging.getLogger(__name__)
global lock
lock = threading.Lock()

def get_tree(args):
    ret=TrainCourseGroup.get_train_course_group()
    return ret.get_list()


def insert(args):
    try:
        lock.acquire()
        ret = {}
        if args['data'] != None:
            data =  set_dict_insert_data(args)
            if data.has_key('parent_code') and data['parent_code'] != None:
                train_course_group = models.HCSLS_TrainCourseGroup().aggregate().project(
                    level_code = 1,
                    train_group_code = 1,
                    level = 1).match("train_group_code == {0}", data['parent_code']).get_item()
                data['level'] = train_course_group['level'] + 1
                train_course_group['level_code'].append(data['train_group_code'])
                data['level_code'] = train_course_group['level_code']
            else:
                data['level'] = 1
                data['level_code'] = [data['train_group_code']]
            ret  =  models.HCSLS_TrainCourseGroup().insert(data)
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
            if data.has_key('parent_code') and data['parent_code'] != None:
                train_course_group = models.HCSLS_TrainCourseGroup().aggregate().project(
                    level_code = 1,
                    train_group_code = 1,
                    level = 1).match("train_group_code == {0}", data['parent_code']).get_item()
                data['level'] = train_course_group['level'] + 1
                train_course_group['level_code'].append(args['data']['train_group_code'])
                data['level_code'] = train_course_group['level_code']
            else:
                data['level'] = 1
                data['level_code'] = [args['data']['train_group_code']]

            ret  =  models.HCSLS_TrainCourseGroup().update(
                data, 
                "train_group_code == {0}",
                args['data']['train_group_code'])
            if ret['data'].raw_result['updatedExisting'] == True:
                ret.update(
                    item = TrainCourseGroup.get_train_course_group().match("train_group_code == {0}", args['data']['train_group_code']).get_item()
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




# def delete(args):
#     try:
#         lock.acquire()
#         ret = {}
#         if args['data'] != None:
#             list_group_code = [x["train_group_code"]for x in args['data']]
#             if TrainCourseGroup.check_exits_courseCode_within_courseGroup(list_group_code) == False:
#                  ret  =  models.HCSLS_TrainCourseGroup().delete("train_group_code in {0}",[x["train_group_code"]for x in args['data']])
#                  lock.release()
#                  return ret
#             else:
#                 lock.release()
#                 return dict(
#                     error = "not allow"
#                     )
#         lock.release()
#         return  dict(
#             error = "request parameter is not exist"
#             )
#     except Exception as ex:
#         lock.release()
#         raise(ex)
def delete(args):
    try:
        lock.acquire()
        ret = {}
        if args['data'] != None:
            #code được chọn
            list_group_code = [x["train_group_code"]for x in args['data']]
            #từ code hiện tại đến các cấp cha
            list_fiter = []
            if len(list_group_code) > 0:
                for x in list_group_code:
                    collection = common.get_collection('HCSLS_TrainCourseGroup').aggregate([
                        {
                            "$match": {
                                "$or":[
                                    { "train_group_code": str(x).format() },
                                    { "train_group_code": { "$in": common.get_collection('HCSLS_TrainCourseGroup').find_one({ "train_group_code": str(x).format() })["level_code"] }}
                                    ]}
                        },
                        {
                            "$project":{
                                "_id": 0,
                                "train_group_code": 1
                          }}
                        ])
                    list_fiter += list(collection)
            else:
                lock.release()
                return dict(
                    error = "train_group_code is not exit"
                )

            #kiểm tra từ code hiện tại đến các cấp cha có group code nào đang được sử dụng không
            #Nếu có 'len(list__workig) > 0' return
            #Không có xử lí delete
            list_kpi_workig = models.HCSLS_TrainCourseGroup().aggregate().project(
                #course_code = 1,
                train_group_code = 1
                ).match("train_group_code in {0}", [x["train_group_code"]for x in list_fiter]).get_list()
            if len(list_kpi_workig) > 0:
                ret = models.HCSLS_TrainCourseGroup().delete("train_group_code in {0}", list_group_code)
                lock.release()
                return ret
            else:
                lock.release()
                return dict(
                    error="TrainGroup is using another PG",
                    items=list_kpi_workig,
                    deleted=0
                )

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
        train_group_code         = (lambda x: x['train_group_code']          if x.has_key('train_group_code')          else None)(args['data']),
        train_group_name         = (lambda x: x['train_group_name']          if x.has_key('train_group_name')          else None)(args['data']),
        train_group_name2        = (lambda x: x['train_group_name2']         if x.has_key('train_group_name2')         else None)(args['data']),
        parent_code      = (lambda x: x['parent_code']       if x.has_key('parent_code')       else None)(args['data']),
        level            = (lambda x: x['level']             if x.has_key('level')             else 1)(args['data']),
        level_code       = (lambda x: x['level_code']        if x.has_key('level_code')        else None)(args['data']),
        ordinal          = (lambda x: x['ordinal']           if x.has_key('ordinal')           else None)(args['data']),
        note             = (lambda x: x['note']              if x.has_key('note')              else None)(args['data']),
        lock             = (lambda x: x['lock']              if x.has_key('lock')              else None)(args['data'])
        
    )

    return ret_dict


def set_dict_update_data(args):
    ret_dict = set_dict_insert_data(args)
    del ret_dict['train_group_code']
    return ret_dict
