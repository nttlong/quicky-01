# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
import qmongo
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


def insert(args):
    from quicky import tenancy
    if args['data'] != None:
        ret = {}
        try:
            lock.acquire()
            user_name = args['data']['login_account']
            check_exist = qmongo.models.auth_user_info.aggregate.project(login_account = 1).match("login_account == {0}", user_name).get_list()

            if len(check_exist) == 0:

                args['data']['username'] = generate_user_id()

                data = dict(
                    username         = args['data']['username'],
                    login_account    = args['data']['login_account'],
                    display_name     = args['data']['display_name'],
                    role_code        = (lambda data: data["role_code"] if data.has_key("role_code") else None)(args['data']),
                    email            = args['data']['email'],
                    is_system        = (lambda data: data["is_system"] if data.has_key("is_system") else False)(args['data']),
                    never_expire     = (lambda data: data["never_expire"] if data.has_key("never_expire") else False)(args['data']),
                    manlevel_from    = (lambda data: data["manlevel_from"] if data.has_key("manlevel_from") else None)(args['data']),
                    manlevel_to      = (lambda data: data["manlevel_to"] if data.has_key("manlevel_to") else None)(args['data']),
                    mobile           = (lambda data: data["mobile"] if data.has_key("mobile") else None)(args['data']),
                    description      = (lambda data: data["description"] if data.has_key("description") else None)(args['data'])
                    )

                ret = qmongo.models.auth_user_info.insert(data)
                if ret.has_key('error') and ret['error'] != None:
                    raise(Exception(ret['error']['code']))

                try:
                    user = User.objects.create_user(
                        username=args['data']['username'],
                        password=args['data']['password'],
                        schema=tenancy.get_schema()
                    )
                    user.save(schema=tenancy.get_schema())
                    lock.release()
                    return ret
                except Exception as ex:
                    qmongo.models.auth_user_info.delete("username == {0}", args['data']['username'])
                    lock.release()
                    return dict(
                        error = "Internal Server Error"
                    )
            lock.release()
            return dict(
                error = "existing login account"
            ) #Already account
        except Exception as ex:
                logger.debug(ex)
                lock.release()
                return ret
    return dict(
            error = "request parameter is not exist"
        )

def update(args):
    from quicky import tenancy
    if args['data'] != None:
        try:
            lock.acquire()
            user_name = args['data']['login_account']
            if qmongo.models.auth_user_info.aggregate.match("_id == {0}", ObjectId(args['data']['_id'])).get_item() != None:

                data = dict(
                    login_account    = args['data']['login_account'],
                    display_name     = args['data']['display_name'],
                    role_code        = (lambda data: data["role_code"] if data.has_key("role_code") else None)(args['data']),
                    email            = args['data']['email'],
                    is_system        = (lambda data: data["is_system"] if data.has_key("is_system") else False)(args['data']),
                    never_expire     = (lambda data: data["never_expire"] if data.has_key("never_expire") else False)(args['data']),
                    manlevel_from    = (lambda data: data["manlevel_from"] if data.has_key("manlevel_from") else None)(args['data']),
                    manlevel_to      = (lambda data: data["manlevel_to"] if data.has_key("manlevel_to") else None)(args['data']),
                    mobile           = (lambda data: data["mobile"] if data.has_key("mobile") else None)(args['data']),
                    description      = (lambda data: data["description"] if data.has_key("description") else None)(args['data'])
                    )

                if args['data']['change_password'] != None and args['data']['change_password'] == True:
                    rs_check = check_password(args['data']['password'], user_name)
                    if not rs_check['result']:
                        u = User.objects.get(username=args['data']['username'])
                        u.set_password(args['data']['password'])
                        u.save(schema=tenancy.get_schema())
                    else:
                        lock.release()
                        return rs_check

                ret = qmongo.models.auth_user_info.update(
                    data,
                    "username == {0}",
                    args['data']['username'])

                lock.release()
                return ret

            lock.release()
            return None #Already account
        except Exception as ex:
                logger.debug(ex)
                lock.release()
                raise(ex)
    return None

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

def delete(args):
    if args['data'] != None:
        try:
            user_names = qmongo.models.auth_user_info.aggregate.project(username = 1).match("_id in {0}", [ObjectId(x["_id"])for x in args['data']]).get_list()

            qmongo.models.auth_user.delete("username in {0}", [x["username"] for x in user_names])
            ret = qmongo.models.auth_user_info.delete("username in {0}", [x["username"]for x in args['data']])
            return ret
        except Exception as ex:
            logger.debug(ex)
            return dict(
                    error = ex.message
                )
    return dict(
            error = "request parameter is not exist"
        )

def get_list_with_searchtext(args):
    if args['data'] != None:
        try:
            searchText      = args['data'].get('search', '')
            pageSize        = args['data'].get('pageSize', 0)
            pageIndex       = args['data'].get('pageIndex', 20)
            sort            = args['data'].get('sort', 20)
            where           = (lambda data: data["where"] if data.has_key("where") else {})(args['data'])

            pageIndex       = (lambda pIndex: pIndex if pIndex != None else 0)(pageIndex)
            pageSize        = (lambda pSize: pSize if pSize != None else 20)(pageSize)

            items = qmongo.models.auth_user_info.aggregate
            items.left_join(qmongo.models.AD_Roles, "role_code", "role_code", "role")
            items.project(
                    login_account       = 1,
                    username            = 1,
                    display_name        = 1,
                    role_code           = 1,
                    role_name           ="switch(case(role_code!='',role.role_name),'')",
                    is_system           = 1,
                    never_expire        = 1,
                    manlevel_from       = 1,
                    manlevel_to         = 1,
                    email               = 1,
                    mobile              = 1,
                    description         = 1,
                    created_on          = 1
                    )

            if(searchText != None):
                items.match("contains(login_account, @name) or contains(display_name, @name) " + \
                    "or contains(role_code, @name) or contains(manlevel_from, @name) " + \
                    "or contains(manlevel_to, @name) or contains(created_on, @name)",name=searchText.strip())

            if(where != None and where != {}):
                try:
                    if where.has_key('filter') and  where.has_key('value') and len(where['filter']) and len(where['value']):
                        items.match(where["filter"],where["value"])
                except Exception as ex:
                    raise(Exception("syntax where error"))

            if(sort != None):
                items.sort(sort)

            return items.get_page(pageIndex, pageSize)
        except Exception as ex:
            raise(ex)

    return dict(
            error = "request parameter is not exist"
        )

def get_user_info_by_user_name(args):
    return qmongo.models.auth_user_info.aggregate.project(display_name = 1, login_account = 1, username = 1).match('username == {0}', args['data']['username']).get_item()

def update_role_code(args):
    try:
        if args['data'] != None:
            lock.acquire()

            if args['data'].has_key('role_code') and args['data'].has_key('users'):
                user_names = [x["username"]for x in args['data']['users']]
                ret = qmongo.models.auth_user_info.update(
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
            ret = qmongo.models.auth_user_info.update(
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
        ret = qmongo.models.auth_user_info.update(
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