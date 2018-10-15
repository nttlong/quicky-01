# -*- coding: utf-8 -*-
from bson import ObjectId
import models
from Query import KPIGroup
import logging
import threading
import common
from hcs_authorization import action_type,authorization
logger = logging.getLogger(__name__)
global lock
lock = threading.Lock()

@authorization.authorise(action=action_type.Action.READ)
def get_tree(args):
    lock = args['data']['lock']
    
    ret = get_competency_group(lock)
    
    return ret.get_list()

@authorization.authorise(common=True)
def get_competency_group(lock):
    if lock != None:
        if (int(lock) == 0):
            lock = False
        elif (int(lock) == 1):
            lock = True
        else: 
            lock = None
    ret = models.TMLS_CompetencyGroup().aggregate();
    ret.left_join(models.auth_user_info(), "created_by", "username", "uc");
    ret.left_join(models.auth_user_info(), "modified_by", "username", "um");

    if lock != None:
        ret.match("lock == {0}", lock);

    ret.project(
        com_group_code = 1,
        com_group_name = 1,
        com_group_name2 = 1,
        parent_code = 1,
        level = 1,
        level_code = 1,
        note = 1,
        ordinal = 1,
        lock = 1,
        created_by="uc.login_account",
        created_on= "created_on",
        modified_on="switch(case(modified_on!='',modified_on),'')",
        modified_by="switch(case(modified_by!='',um.login_account),'')",
        )
    ret.sort(dict(com_group_code = 1,
        ordinal = 1))

    return ret

@authorization.authorise(action=action_type.Action.CREATE)
def insert(args):
    try:
        lock.acquire()
        ret = {}
        if args['data'] != None:
            data = set_dict_insert_data(args)
            if data.has_key('parent_code') and data['parent_code'] != None:
                parent_com_group_code = models.TMLS_CompetencyGroup().aggregate().project(
                    level_code = 1, 
                    com_group_code = 1,
                    level = 1).match("com_group_code == {0}", data['parent_code']).get_item()
                data['level'] = parent_com_group_code['level'] + 1
                parent_com_group_code['level_code'].append(data['com_group_code'])
                data['level_code'] = parent_com_group_code['level_code']
            else:
                data['level'] = 1
                data['level_code'] = [data['com_group_code']]
            ret = models.TMLS_CompetencyGroup().insert(data)
            lock.release()
            return ret

        lock.release()
        return dict(error = "request parameter is not exist")
    except Exception as ex:
        lock.release()
        raise(ex)

@authorization.authorise(action=action_type.Action.WRITE)
def update(args):
    try:
        lock.acquire()
        ret = {}
        if args['data'] != None:
            data = set_dict_update_data(args)
            if data.has_key('parent_code') and data['parent_code'] != None:
                parent_com_group_code = models.TMLS_CompetencyGroup().aggregate().project(
                    level_code = 1, 
                    com_group_code = 1,
                    level = 1).match("com_group_code == {0}", data['parent_code']).get_item()
                data['level'] = parent_com_group_code['level'] + 1
                parent_com_group_code['level_code'].append(args['data']['com_group_code'])
                data['level_code'] = parent_com_group_code['level_code']
            else:
                data['level'] = 1
                data['level_code'] = [args['data']['com_group_code']]

            ret = models.TMLS_CompetencyGroup().update(data, 
                "com_group_code == {0}", 
                args['data']['com_group_code'])
            if ret['data'].raw_result['updatedExisting'] == True:
                ret.update(item = get_competency_group(args["data"]["lock"]).match("com_group_code == {0}", args['data']['com_group_code']).get_item())
            lock.release()
            return ret

        lock.release()
        return dict(error = "request parameter is not exist")
    except Exception as ex:
        lock.release()
        raise(ex)

@authorization.authorise(action=action_type.Action.DELETE)
def delete(args):
    try:
        lock.acquire()
        ret = {}
        if args['data'] != None:
            #code được chọn
            list_group_code = [x["com_group_code"]for x in args['data']]
            #từ code hiện tại đến các cấp cha
            list_fiter = []
            if len(list_group_code) > 0:
                for x in list_group_code:
                    collection = common.get_collection('TMLS_CompetencyGroup').aggregate([
                        { 
                            "$match": { 
                                "$or":[
                                    { "com_group_code": str(x).format() },
                                    { "com_group_code": { "$in": common.get_collection('TMLS_CompetencyGroup').find_one({ "com_group_code": str(x).format() })["level_code"] }}
                                    ]}
                        },
                        {
                            "$project":{
                                "_id": 0,
                                "com_group_code": 1
                          }}
                        ])
                    list_fiter += list(collection)
            else:
                lock.release()
                return dict(
                    error = "com_group_code is not exsit"
                )

            #kiểm tra từ code hiện tại đến các cấp cha có group code nào đang được sử dụng không
            #Nếu có 'len(list_com_workig) > 0' return
            #Không có xử lí delete
            list_com_workig = models.TMLS_Competency().aggregate().project(
                com_code = 1,
                com_group_code = 1
                ).match("com_group_code in {0}", [x["com_group_code"]for x in list_fiter]).get_list()
            if len(list_com_workig) > 0:
                lock.release()
                return dict(
                    error = "CompetencyGroup is using another PG",
                    items = list_com_workig,
                    deleted = 0
                )
            else:
                ret  =  models.TMLS_CompetencyGroup().delete("com_group_code in {0}", list_group_code)
                lock.release()
                return ret

        lock.release()
        return dict(
            error = "request parameter is not exist"
        )
    except Exception as ex:
        lock.release()
        raise(ex)


@authorization.authorise(common=True)
def set_dict_insert_data(args):
    ret_dict = dict()

    ret_dict.update(
        com_group_code   = (lambda x: x['com_group_code']    if x.has_key('com_group_code')    else None)(args['data']),
        com_group_name   = (lambda x: x['com_group_name']    if x.has_key('com_group_name')    else None)(args['data']),
        com_group_name2  = (lambda x: x['com_group_name2']   if x.has_key('com_group_name2')   else None)(args['data']),
        parent_code      = (lambda x: x['parent_code']       if x.has_key('parent_code')       else None)(args['data']),
        level            = (lambda x: x['level']             if x.has_key('level')             else 1)(args['data']),
        level_code       = (lambda x: x['level_code']        if x.has_key('level_code')        else None)(args['data']),
        ordinal          = (lambda x: x['ordinal']           if x.has_key('ordinal')           else None)(args['data']),
        note             = (lambda x: x['note']              if x.has_key('note')              else None)(args['data']),
        lock             = (lambda x: x['lock']              if x.has_key('lock')              else None)(args['data']))

    return ret_dict

@authorization.authorise(common = True)
def set_dict_update_data(args):
    ret_dict = set_dict_insert_data(args)
    del ret_dict['com_group_code']
    return ret_dict
