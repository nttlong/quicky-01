# -*- coding: utf-8 -*-
#from bson import ObjectId
import models
import common
import datetime
#import TM_SetupProcessApproveLevel

def get_list_with_process_id(args):
    try:
        if args['data'] != None and args['data'].has_key('process_id'):
            items = models.TM_SetupProcess().aggregate()
            items.left_join(models.auth_user_info(), "created_by", "username", "uc")
            items.left_join(models.auth_user_info(), "modified_by", "username", "um")
            items.project(
                process_id=1,
                process_name=1,
                is_not_apply_process=1,
                max_approve_level=1,
                is_approve_by_dept=1,
                is_require_reason=1,
                is_require_when_approve=1,
                is_require_when_reject=1,
                is_show_list_approver=1,
                is_reselect_approver=1,
                is_require_attach_file=1,
                file_size_limit=1,
                exclude_file_types=1,
                is_email_cancel=1,
                is_email_delete=1,
                is_email_instead=1,
                email_send_code=1,
                email_send_to=1,
                email_send_cc=1,
                email_send_more=1,
                email_cancel_code=1,
                email_cancel_to=1,
                email_cancel_cc=1,
                email_cancel_more=1,
                email_delete_code=1,
                email_delete_to=1,
                email_delete_cc=1,
                email_delete_more=1,
                email_instead_code=1,
                email_instead_to=1,
                email_instead_cc=1,
                email_instead_more=1,
                is_send_email_pronto=1,
                is_send_email_once=1,
                send_email_once_from_hour=1,
                send_email_once_to_hour=1,
                created_by="uc.login_account",
                created_on=1,
                modified_on="switch(case(modified_on!='',modified_on),'')",
                modified_by="switch(case(modified_by!='',um.login_account),'')",
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

    items = models.TM_SetupProcess().aggregate()
    items.left_join(models.auth_user_info(), "created_by", "username", "uc")
    items.left_join(models.auth_user_info(), "modified_by", "username", "um")
    items.project(
        process_id=1,
        process_name=1,
        is_not_apply_process=1,
        max_approve_level=1,
        is_approve_by_dept=1,
        is_require_reason=1,
        is_require_when_approve=1,
        is_require_when_reject=1,
        is_show_list_approver=1,
        is_reselect_approver=1,
        is_require_attach_file=1,
        file_size_limit=1,
        exclude_file_types=1,
        is_email_cancel=1,
        is_email_delete=1,
        is_email_instead=1,
        email_send_code=1,
        email_send_to=1,
        email_send_cc=1,
        email_send_more=1,
        email_cancel_code=1,
        email_cancel_to=1,
        email_cancel_cc=1,
        email_cancel_more=1,
        email_delete_code=1,
        email_delete_to=1,
        email_delete_cc=1,
        email_delete_more=1,
        email_instead_code=1,
        email_instead_to=1,
        email_instead_cc=1,
        email_instead_more=1,
        is_send_email_pronto=1,
        is_send_email_once=1,
        send_email_once_from_hour=1,
        send_email_once_to_hour=1,
        created_by="uc.login_account",
        created_on="created_on",
        modified_on="switch(case(modified_on!='',modified_on),'')",
        modified_by="switch(case(modified_by!='',um.login_account),'')"
    )

    if(searchText != None) :
        items.match("contains(process_name, @name)", name=searchText)

    if(sort != None):
        items.sort(sort)
        
    return items.get_page(pageIndex, pageSize)

def insert(args):
    if args['data'] != None:
        # Quy trình duyệt cuối kỳ phát sinh data cho UI Tab cấp duyệt/Cách tính điểm đánh giá
        # process_id = "2"
        if args['data']['process_id'] == "2":
            args['data']['score_by_coeff'] = [
                {
                    "approve_level": 0,
                    "coeff": 1
                }
            ]
            for x in range(args['data']['max_approve_level']):
                args['data']['score_by_coeff'].append({
                    "approve_level":range(args['data']['max_approve_level']).index(x) + 1,
                    "coeff": 1
                })
        ret = models.TM_SetupProcess().insert(args['data'])
        return ret
    return None

def update(args):
    process_id = ""
    current_process = None
    if args['data'] != None:
        if args['data']['process_id'] == None:
            return None
        else:
            if(args['data'].has_key('process_id')):
                process_id = args['data']['process_id']
                if process_id == "2":
                    current_process = list(common.get_collection("TM_SetupProcess").aggregate(
                        [
                            {"$project":{
                                "process_id":1,
                                "max_approve_level": 1,
                                "score_by_coeff": 1
                                }
                            },
                            {"$match":{
                                "process_id": args['data']['process_id']
                                }
                            }
                        ]
                    ))[0]
                    #Tăng cấp duyệt
                    if current_process['max_approve_level'] < args['data']['max_approve_level']:
                        max_level = args['data']['max_approve_level'] - current_process['max_approve_level']
                        for x in range(max_level):
                            current_process['score_by_coeff'].append({
                                "approve_level":current_process['max_approve_level'] + range(max_level).index(x) + 1,
                                "coeff": 1
                            })
                        models.TM_SetupProcess().update(
                            {
                                "score_by_coeff": current_process['score_by_coeff']
                            },
                            "process_id == @process_id",
                            process_id = args['data']['process_id']
                        )
                    #Giảm cấp duyệt
                    elif current_process['max_approve_level'] > args['data']['max_approve_level']:
                        max_level = current_process['max_approve_level'] - args['data']['max_approve_level']
                        for x in range(max_level):
                            current_process['score_by_coeff'].pop(current_process['max_approve_level'] - (range(max_level).index(x)))
                        models.TM_SetupProcess().update(
                            {
                                "score_by_coeff": current_process['score_by_coeff']
                            },
                            "process_id == @process_id",
                            process_id=args['data']['process_id']
                        )

                args['data'].pop('process_id')
            ret = models.TM_SetupProcess().update(
            args['data'],
            "process_id==@process_id",
            dict(
                process_id = process_id
            ))
            return ret
    return None

def delete(args):
    if args['data'] != None:
        ret = models.TM_SetupProcess().delete("process_id in {0}", [x["process_id"] for x in args['data']])
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
    count_approve_level = common.get_collection("TM_SetupProcessApproveLevel").find({
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
                    args['data']['email_approve_more'] = None

                    args['data']['email_reject_code'] = None
                    args['data']['email_reject_to'] = None
                    args['data']['email_reject_cc'] = None
                    args['data']['email_reject_more'] = None

                    args['data']['email_approve_cancel_code'] = None
                    args['data']['email_approve_cancel_to'] = None
                    args['data']['email_approve_cancel_cc'] = None
                    args['data']['email_approve_cancel_more'] = None

                    args['data']['default_approver_code'] = None
                    args['data']['not_receive_email'] = False
                    args['data']['created_on'] = None #str(datetime.datetime.now())
                    args['data']['created_by'] = "admin" #models.auth_user_info()["login_account"]
                    args['data']['modified_on'] = None
                    args['data']['modified_by'] = None
                    ret = models.TM_SetupProcessApproveLevel().insert(args['data'])
                    i += 1
                return ret
            elif count_approve_level > max_approve_level: #giảm số cấp duyệt
                ret = models.TM_SetupProcessApproveLevel().delete("approve_level > {0} and process_id == {1}", max_approve_level, int(args['data']['process_id']))
                update_data = {}
                for x in range(count_approve_level - max_approve_level):
                    update_data.update({"appover_code." + str(max_approve_level + range(count_approve_level - max_approve_level).index(x)): None})

                common.get_collection('TM_SetupProcessApproverEmp').update_many(
                    {
                        'process_id': args['data']['process_id']
                    },
                    {
                        '$set': update_data
                    }
                )
                common.get_collection('TM_SetupProcessApproverDept').update_many(
                    {
                        'process_id':args['data']['process_id']
                    },
                    {
                        '$set': update_data
                    }
                )
                return ret
    return None

def get_score_coeff_by_process_id(args):
    try:
        return models.TM_SetupProcess().aggregate().project(
            process_id = 1,
            process_level_apply_for = 1,
            score_by = 1,
            score_by_coeff = 1
        ).match("process_id == @process_id", process_id = args['data']['process_id']).get_item()
    except Exception as ex:
        raise ex

def update_score_by_coeff_by_process_id(args):
    try:
        ret = {}
        process_id = args['data']['process_id']
        del args['data']['process_id']
        if args['data']['score_by'] != 4:
            del args['data']['score_by_coeff']
        ret = models.TM_SetupProcess().update(
            args['data'],
            "process_id == @process",
            process = process_id
        )
        return ret
    except Exception as ex:
        raise ex