# -*- coding: utf-8 -*-
from bson import ObjectId
import models
import common
import datetime
import LMS_SetupProcessApproveLevel
import qmongo
def get_list_with_process_id(args):
    try:
        if args['data'] != None and args['data'].has_key('process_id'):
            items =  qmongo.models.LMS_SetupProcess.aggregate.project(
                process_id = 1,
                process_name = 1,
                is_not_apply_process = 1,
                max_approve_level = 1,
                is_select_approver = 1,
                is_approve_by_dept = 1,
                is_require_reason = 1,
                is_require_when_approve = 1,
                is_require_when_reject = 1,
                sender_value = 1,
                file_size_limit = 1,
                exclude_file_types = 1,
                email_send_code = 1,
                email_send_to = 1,
                email_send_cc = 1,
                is_send_email_pronto  = 1,
                is_send_email_once = 1,
                is_send_email_once_from_hour = 1,
                is_send_email_once_to_hour= 1,
                created_by=1,
                created_on=1,
                modified_on=1,
                modified_by=1
                ).match("process_id == {0}", args['data']['process_id'])    
        return items.get_item()
        raise(Exception("not found process_id"))
    except Exception as ex:
        raise(ex)

def get_list_with_searchtext(args):
    searchText = args['data'].get('search', '')
    pageSize = args['data'].get('pageSize', 0)
    pageIndex = args['data'].get('pageIndex', 20)
    sort = args['data'].get('sort', 20)

    pageIndex = (lambda pIndex: pIndex if pIndex != None else 0)(pageIndex)
    pageSize = (lambda pSize: pSize if pSize != None else 20)(pageSize)

    items = qmongo.models.LMS_SetupProcess.aggregate
    items.left_join(qmongo.models.models.auth_user_info, "created_by", "username", "uc")
    items.left_join(qmongo.models.models.auth_user_info, "modified_by", "username", "um")
    items.project(
            process_id = 1,
            process_name = 1,
            function_id = 1,
            is_not_apply_process = 1,
            max_approve_level = 1,
            is_select_approver = 1,
            is_approve_by_dept = 1,
            is_require_reason = 1,
            is_require_when_approve = 1,
            is_require_when_reject = 1,
            sender_value = 1,
            file_size_limit = 1,
            exclude_file_types = 1,
            email_send_code = 1,
            email_send_to = 1,
            email_send_cc = 1,
            is_send_email_pronto  = 1,
            is_send_email_once = 1,
            is_send_email_once_from_hour = 1,
            is_send_email_once_to_hour= 1,
            created_by="uc.login_account",
            created_on="created_on",
            modified_on="switch(case(modified_on!='',modified_on),'')",
            modified_by="switch(case(modified_by!='',um.login_account),'')"
            )

    if(searchText != None):
        items.match("contains(process_name, @name)",name=searchText)

    if(sort != None):
        items.sort(sort)
        
    return items.get_page(pageIndex, pageSize)

def insert(args):
    if args['data'] != None:
        ret = qmongo.models.LMS_SetupProcess.insert(args['data'])
        return ret
    return None

def update(args):
    process_id = ""
    if args['data'] != None:
        if args['data']['process_id'] == None:
            return None
        else:
            if(args['data'].has_key('process_id')):
                process_id = args['data']['process_id']
                args['data'].pop('process_id')
            ret = qmongo.models.LMS_SetupProcess.update(
            args['data'],
            "process_id==@process_id",
            dict(
                process_id = process_id
            ))
            return ret
    return None

def delete(args):
    if args['data'] != None:
        ret = qmongo.models.LMS_SetupProcess.delete("process_id in {0}", [x["process_id"] for x in args['data']])
        return ret
    return None

def set_dict_data(args):
    data = dict(
        process_id     =     args['data']['process_id'],
        process_name     =     args['data']['process_name'],
        is_not_apply_process    =     (lambda x: x['is_not_apply_process'] if x.has_key('is_not_apply_process') else None)(args['data']),
        function_id    =     (lambda x: x['function_id'] if x.has_key('function_id') else None)(args['data']),
        max_approve_level    =     (lambda x: x['max_approve_level'] if x.has_key('max_approve_level') else None)(args['data']),
        is_select_approver         =     (lambda x: x['is_select_approver'] if x.has_key('is_select_approver') else None)(args['data']),
        is_approve_by_dept               =     (lambda x: x['is_approve_by_dept'] if x.has_key('is_approve_by_dept') else None)(args['data']),
        is_require_reason          =     (lambda x: x['is_require_reason'] if x.has_key('is_require_reason') else None)(args['data']),
        is_require_when_approve      =     (lambda x: x['is_require_when_approve'] if x.has_key('is_require_when_approve') else None)(args['data']),
        is_require_when_reject      =     (lambda x: x['is_require_when_reject'] if x.has_key('is_require_when_reject') else None)(args['data']),
        sender_value    =     (lambda x: x['sender_value'] if x.has_key('sender_value') else None)(args['data']),
        file_size_limit  =     (lambda x: x['department_address'] if x.has_key('file_size_limit') else None)(args['data']),
        exclude_file_types         =     (lambda x: x['exclude_file_types'] if x.has_key('exclude_file_types') else None)(args['data']),
        email_send_code       =     (lambda x: x['email_send_code'] if x.has_key('email_send_code') else None)(args['data']),
        email_send_to       =     (lambda x: x['email_send_to'] if x.has_key('email_send_to') else None)(args['data']),
        email_send_cc          =     (lambda x: x['email_send_cc'] if x.has_key('email_send_cc') else None)(args['data']),
        is_send_email_pronto             =     (lambda x: x['is_send_email_pronto'] if x.has_key('is_send_email_pronto') else None)(args['data']),
        is_send_email_once       =     (lambda x: x['is_send_email_once'] if x.has_key('is_send_email_once') else None)(args['data']),
        is_send_email_once_from_hour         =     (lambda x: x['is_send_email_once_from_hour'] if x.has_key('is_send_email_once_from_hour') else None)(args['data']),
        is_send_email_once_to_hour       =     (lambda x: x['is_send_email_once_to_hour'] if x.has_key('is_send_email_once_to_hour') else None)(args['data']),       
    )
    return data

def generate_list_approve_by_max_approve_level(args):
    #số cấp duyệt đã có
    count_approve_level = common.get_collection("LMS_SetupProcessApproveLevel").find({
        "process_id" : int(args['data']['process_id'])
        }).count()
    
    if args['data'] != None:
        max_approve_level = args['data']['max_approve_level']
        if max_approve_level == None:
            return None
        else:
            if count_approve_level < max_approve_level: #tăng số cấp duyệt
                i = count_approve_level + 1
                while (i <= max_approve_level):
                    print(i)
                    args['data']['rec_id'] = common.generate_guid()
                    args['data']['process_id'] = int(args['data']['process_id'])
                    args['data']['approve_level'] = i
                    args['data']['approver_value'] = None
                    args['data']['email_approve_code'] = None
                    args['data']['email_approve_to'] = None
                    args['data']['email_approve_cc'] = None
                    args['data']['email_reject_code'] = None
                    args['data']['email_reject_to'] = None
                    args['data']['email_reject_cc'] = None
                    args['data']['default_approver_code'] = None
                    args['data']['not_receive_email'] = False
                    args['data']['created_on'] = None #str(datetime.datetime.now())
                    args['data']['created_by'] = "admin" #models.models.auth_user_info()["login_account"]
                    args['data']['modified_on'] = None
                    args['data']['modified_by'] = None
                    ret =  qmongo.models.LMS_SetupProcessApproveLevel.insert(args['data'])
                    i += 1
                return ret
            elif count_approve_level > max_approve_level: #giảm số cấp duyệt
                ret = qmongo.models.LMS_SetupProcessApproveLevel.delete("approve_level > {0} and process_id == {1}", max_approve_level, int(args['data']['process_id']))
                return ret
    return None

def set_dict_data_approve_level(args):
    data = dict(
        process_id     =     args['process_id'],
        approve_level     =     (lambda x: x['approve_level'] if x.has_key('approve_level') else None)(args),
        approver_value    =     (lambda x: x['approver_value'] if x.has_key('approver_value') else None)(args),
        email_approve_code    =     (lambda x: x['email_approve_code'] if x.has_key('email_approve_code') else None)(args),
        email_approve_to    =     (lambda x: x['email_approve_to'] if x.has_key('email_approve_to') else None)(args),
        email_approve_cc         =     (lambda x: x['email_approve_cc'] if x.has_key('email_approve_cc') else None)(args),
        email_reject_code               =     (lambda x: x['email_reject_code'] if x.has_key('email_reject_code') else None)(args),
        email_reject_to          =     (lambda x: x['email_reject_to'] if x.has_key('email_reject_to') else None)(args),
        email_reject_cc      =     (lambda x: x['email_reject_cc'] if x.has_key('email_reject_cc') else None)(args),
        default_approver_code      =     (lambda x: x['default_approver_code'] if x.has_key('default_approver_code') else None)(args),
        not_receive_email    =     (lambda x: x['not_receive_email'] if x.has_key('not_receive_email') else None)(args)
    )
    return data