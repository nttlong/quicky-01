# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from bson import ObjectId
import uuid
import models
import datetime
import logging
import threading
import re
logger = logging.getLogger(__name__)
global lock
lock = threading.Lock()

def generate_user_id():
    return str(uuid.uuid4())


def get_list_with_searchtext(args):
    searchText = args['data'].get('search', '')
    pageSize = args['data'].get('pageSize', 0)
    pageIndex = args['data'].get('pageIndex', 20)
    sort = args['data'].get('sort', 20)

    pageIndex = (lambda pIndex: pIndex if pIndex != None else 0)(pageIndex)
    pageSize = (lambda pSize: pSize if pSize != None else 20)(pageSize)

    items = models.HCSLS_TrainProfession().aggregate()
    items.left_join(models.models_per.auth_user_info(), "created_by", "username", "uc")
    items.left_join(models.models_per.auth_user_info(), "modified_by", "username", "um")
    items.project(
        profession_code=1,
        profession_name=1,
        profession_name2=1,
        field_code=1,
        note=1,
        lock=1,
        ordinal=1,
        created_by="uc.login_account",
        created_on="created_on",
        modified_on="switch(case(modified_on!='',modified_on),'')",
        modified_by="switch(case(modified_by!='',um.login_account),'')",
    )

    # if(searchText != None):
    #     items.match("contains(profession_name, @name)",name=searchText)
    if (searchText != None):
        items.match("contains(profession_code, @name) or contains(profession_name, @name)" + \
                  " or contains(note, @name) or contains(ordinal, @name)", name=searchText.strip())

    if(sort != None):
        items.sort(sort)

    return items.get_page(pageIndex, pageSize)

def insert(args):
    try:
        lock.acquire()
        ret = {}
        if args['data'] != None:
            data =  set_dict_insert_data(args)
            ret  =  models.HCSLS_TrainProfession().insert(data)
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
        profession_code=(lambda x: x['profession_code'] if x.has_key('profession_code') else None)(args['data']),
        profession_name=(lambda x: x['profession_name'] if x.has_key('profession_name') else None)(args['data']),
        profession_name2=(lambda x: x['profession_name2'] if x.has_key('profession_name2') else None)(args['data']),
        field_code=(lambda x: x['field_code'] if x.has_key('field_code') else None)(args['data']),
        ordinal=(lambda x: x['ordinal'] if x.has_key('ordinal') else None)(args['data']),
        note=(lambda x: x['note'] if x.has_key('note') else None)(args['data']),
        lock=(lambda x: x['lock'] if x.has_key('lock') else None)(args['data']),
    )

    return ret_dict

def update(args):
    try:
        lock.acquire()
        ret = {}
        if args['data'] != None:
            data =  set_dict_update_data(args)
            ret  =  models.HCSLS_TrainProfession().update(
                data, 
                "_id == {0}", 
                ObjectId(args['data']['_id']))
            if ret['data'].raw_result['updatedExisting'] == True:
                ret.update(
                    item = models.HCSLS_TrainProfession().aggregate().match("_id == {0}", ObjectId(args['data']['_id'])).get_item()
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
            ret = models.HCSLS_TrainProfession().delete("profession_code in {0}", [x["profession_code"] for x in args['data']])
            lock.release()
            return ret

        lock.release()
        return dict(
            error = "request parameter is not exist"
        )
    except Exception as ex:
        lock.release()
        raise(ex)

def set_dict_update_data(args):
    ret_dict = set_dict_insert_data(args)
    del ret_dict['profession_code']
    return ret_dict

def check_password(password, user_name):
    from .. import SystemConfig
    accountConfig = SystemConfig.get()
    rs = {
        "result": False,
        "error": []
    }

    #Check min_len
    if (accountConfig.apply_minLength == True):
        if (len(password) < accountConfig.min_len):
            rs["result"] = True
            rs["error"].append(
                {
                    "config":"apply_minLength",
                    "require":accountConfig.apply_minLength,
                    "require_length":accountConfig.min_len
                })
            return rs

    #Check max_len
    if (accountConfig.apply_maxLength == True):
        if (len(password) > accountConfig.max_len):
            rs.result = True
            rs["error"].append({
                    "config":"apply_maxLength",
                    "require":accountConfig.apply_maxLength,
                    "require_length":accountConfig.max_len
                })
            return rs

    #Check cho phép password chứa user login
    if (accountConfig.not_user_in_password == True):
        if user_name in password:
            rs["result"] = True
            rs["error"].append({
                    "config":"not_user_in_password",
                    "require":accountConfig.not_user_in_password
                })
            return rs

    #Check uppercase
    if (accountConfig.is_has_upper_char == True):
        if ([1 if letter.isupper() else 0 for letter in password] or []).count(1) < accountConfig.num_of_upper:
            rs["result"] = True
            rs["error"].append({
                    "config":"is_has_upper_char",
                    "require":accountConfig.is_has_upper_char,
                    "require_length":accountConfig.num_of_upper
                })
            return rs

    #Check lower
    if (accountConfig.is_has_lower_char == True):
        if ([1 if letter.islower() else 0 for letter in password] or []).count(1) < accountConfig.num_of_lower:
            rs["result"] = True
            rs["error"].append({
                    "config":"is_has_lower_char",
                    "require":accountConfig.is_has_lower_char,
                    "require_length":accountConfig.num_of_lower
                })
            return rs

    #Check symbol
    if (accountConfig.is_has_symbols == True):
        if re.search(r"(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])", password) == None:
            rs["result"] = True
            rs["error"].append({
                    "config":"is_has_symbols",
                    "require":accountConfig.is_has_symbols,
                    "require_length":accountConfig.num_of_symbol
                })
            return rs

    return rs

def get_user_info_by_user_name(args):
    return models.models_per.auth_user_info().aggregate().project(display_name = 1, login_account = 1, username = 1).match('username == {0}', args['data']['username']).get_item()

def update_role_code(args):
    try:
        if args['data'] != None:
            lock.acquire()

            if args['data'].has_key('role_code') and args['data'].has_key('users'):
                user_names = [x["username"]for x in args['data']['users']]
                ret = models.models_per.auth_user_info().update(
                    dict(
                        role_code = args['data']['role_code']
                        ),
                    "username in {0}",
                    user_names)

                lock.release()
                return ret

        return dict(
            error = "request parameter is not exist"
        )

    except Exception as ex:
        logger.debug(ex)
        lock.release()
        raise(ex)

def remove_role_code_by_user(args):
    try:
        lock.acquire()
        if args['data'].has_key('users'):
            user_names = [x["username"]for x in args['data']['users']]
            ret = models.models_per.auth_user_info().update(
                dict(
                    role_code = None
                    ),
                "username in {0}",
                user_names)

            lock.release()
            return ret
        return dict(
            error = "request parameter is not exist"
        )
    except Exception as ex:
        logger.debug(ex)
        lock.release()
        raise(ex)

def remove_role_code_by_role(roles):
    try:
        lock.acquire()
        ret = models.models_per.auth_user_info().update(
            dict(
                role_code = None
                ),
            "role_code in {0}",
            roles)

        lock.release()
        return ret
    except Exception as ex:
        logger.debug(ex)
        lock.release()
        raise(ex)