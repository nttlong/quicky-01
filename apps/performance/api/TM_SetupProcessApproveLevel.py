# -*- coding: utf-8 -*-
import models
import datetime
import common
import quicky

def get_list_approve_level_by_process_id(args):
    searchText = args['data'].get('search', '')
    pageSize = args['data'].get('pageSize', 0)
    pageIndex = args['data'].get('pageIndex', 20)
    sort = args['data'].get('sort', 20)

    pageIndex = (lambda pIndex: pIndex if pIndex != None else 0)(pageIndex)
    pageSize = (lambda pSize: pSize if pSize != None else 20)(pageSize)

    items = models.TM_SetupProcessApproveLevel().aggregate()

    # items.left_join(models.SYS_VW_ValueList(), "email_approve_to", "value", "email_approve")
    # items.match("(email_approve.list_name == @list_name and email_approve.language == @lan) or email_approve_to == @email_approve_to",
    #             list_name="LSendEmail", lan= common.get_language(), email_approve_to = None)
    # items.left_join(models.SYS_VW_ValueList(), "email_reject_to", "value", "email_reject")
    # items.match("(email_reject.list_name == @list_name and email_reject.language == @lan) or email_reject_to == @email_reject_to",
    #             list_name="LSendEmail", lan=common.get_language(), email_reject_to = None)
    items.left_join(models.SYS_VW_ValueList(), "approver_value", "value", "appr_val")
    items.match("(appr_val.list_name == @list_name and appr_val.language == @lan) or approver_value == @approver_value",
        list_name="PERF_Approver", lan=common.get_language(), approver_value=None)

    items.left_join(models.auth_user_info(), "created_by", "username", "uc")
    items.left_join(models.auth_user_info(), "modified_by", "username", "um")
    items.project(
            rec_id = 1,
            process_id=1,
            approve_level=1,
            approver_value=1,
            approver_value_display="switch(case(appr_val.caption!='',appr_val.caption),'')",
            email_approve_code=1,
            email_approve_to=1,
            #email_approve_to_name="switch(case(email_approve.value!='',email_approve.value),'')",
            email_approve_cc=1,
            email_approve_more=1,
            email_reject_code=1,
            email_reject_to=1,
            #email_reject_to_name="switch(case(email_reject.value!='',email_reject.value),'')",
            email_reject_cc=1,
            email_reject_more=1,
            email_approve_cancel_code=1,
            email_approve_cancel_to=1,
            email_approve_cancel_cc=1,
            email_approve_cancel_more=1,
            email_reject_cancel_code=1,
            email_reject_cancel_to=1,
            email_reject_cancel_cc=1,
            email_reject_cancel_more=1,
            default_approver_code=1,
            not_receive_email=1,
            created_by="uc.login_account",
            created_on="created_on",
            modified_on="switch(case(modified_on!='',modified_on),'')",
            modified_by="switch(case(modified_by!='',um.login_account),'')"
            ).match("process_id == {0}", int(args['data']['process_id']))

    if(searchText != None):
        items.match("contains(process_name, @name)",name=searchText)

    if(sort != None):
        items.sort(sort)
        
    return items.get_page(pageIndex, pageSize)

def insert(args):
    if args['data'] != None:
        ret = models.LMS_SetupProcess().insert(args['data'])
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
            ret = models.TM_SetupProcessApproveLevel().update(
            args['data'],
            "rec_id == @rec_id",
            rec_id = args['data']['rec_id'])
            return ret
    return None

def delete(args):
    if args['data'] != None:
        ret = models.LMS_SetupProcess().delete("process_id in {0}", [x["process_id"] for x in args['data']])
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