# -*- coding: utf-8 -*-
from .. import models
from .. import common
import qmongo
import datetime

def get_give_target_list_main(args):
    try:
        db = common.get_db_context()
        searchText = args['data'].get('search', '')
        pageSize = args['data'].get('pageSize', 0)
        pageIndex = args['data'].get('pageIndex', 20)
        sort = args['data'].get('sort', 20)

        pageIndex = (lambda pIndex: pIndex if pIndex != None else 0)(pageIndex)
        pageSize = (lambda pSize: pSize if pSize != None else 20)(pageSize)
        search = (lambda x: x.strip() if searchText != None else "")(searchText)

        p_pagi_condition = {
            "page_index": pageIndex,
            "page_size": pageSize,
            "sort": sort,
            "search": search
        }
        ret = db.system_js.TMPER_AprPeriod_FN_TMPER_AprPeriod_GetListMainGiveTarget(common.get_current_schema(),
                                                                      "PERF",
                                                                      p_pagi_condition
                                                                      )
        return ret
    except Exception as ex:
        raise ex

def get_empNotApr_by_apr_period(args):
    searchText = args['data'].get('search', '')
    pageSize = args['data'].get('pageSize', 0)
    pageIndex = args['data'].get('pageIndex', 20)
    sort = args['data'].get('sort', 20)

    ret=qmongo.models.TMPER_AprPeriod.aggregate
    ret.unwind("apr_period_emp_out", False)
    ret.left_join(qmongo.models.auth_user_info, "apr_period_emp_out.created_by", "username", "uc")
    ret.left_join(qmongo.models.auth_user_info, "apr_period_emp_out.modified_by", "username", "um")
    ret.left_join(qmongo.models.HCSEM_Employees, "apr_period_emp_out.employee_code", "employee_code", "ee")

    ret.project(
        apr_period="apr_period",
        apr_year="apr_year",
        employee_code="apr_period_emp_out.employee_code",
        department_code="apr_period_emp_out.department_code",
        job_w_code="apr_period_emp_out.job_w_code",
        reason="apr_period_emp_out.reason",
        note="apr_period_emp_out.note",
        created_by="uc.login_account",
        created_on="apr_period_emp_out.created_on",
        modified_on="switch(case(apr_period_emp_out.modified_on!='',apr_period_emp_out.modified_on),'')",
        modified_by="switch(case(apr_period_emp_out.modified_by!='',um.login_account),'')",
        employee_name="switch(case(apr_period_emp_out.employee_code!='',concat(ee.last_name, ' ' , ee.first_name)),'')",
    )
    ret.match("apr_period == {0} and apr_year == {1}", args['data']['apr_period'], args['data']['apr_year'])
    if(searchText != None and searchText!=''):
        ret.match("contains(reason,{0})"
                  + "or contains(job_w_code,{0}) or contains(employee_code,{0}) or contains(note,{0}) "
                  + "or contains(department_code,{0}) or contains(job_working,{0})"
                  ,searchText)

    if (sort != None):
        ret.sort(sort)
    return ret.get_page(pageIndex, pageSize)

def update_apr_period_emp_out(args):
    try:
        ret = {}
        if args['data'] != None:
            if args['data'].has_key('employee_code'):
                check_exist = check_exist_apr_period_emp_out(args)
                if check_exist != None:
                    emp_out = set_dict_update_apr_period_emp_out(args['data'])
                    ret = update_emp_out(args, emp_out)

            return ret

        return dict(
            error = "request parameter is not exist"
        )
    except Exception as ex:
        raise(ex)

def update_apr_period_emp_out_multi(args):
    try:
        ret = {}
        if args['data'] != None:
            if args['data'].has_key('apr_period_emp_out'):
                common.get_collection("TMPER_AprPeriod").update(
                    {
                        "apr_period": args['data']['apr_period'],
                        "apr_year": args['data']['apr_year'],
                    },
                    {
                        '$set': {
                            "apr_period_emp_out": args['data']['apr_period_emp_out']
                        }
                    },
                    True
                )

            return ret

        return dict(
            error = "request parameter is not exist"
        )
    except Exception as ex:
        raise(ex)


def set_dict_update_apr_period_emp_out(args):
    ret_dict = set_dict_insert_apr_period_emp_out(args)
    ret_dict['modified_on'] = datetime.datetime.now()
    ret_dict['modified_by'] = common.get_user_id()
    return ret_dict

def set_dict_insert_apr_period_emp_out(args):
    ret_dict = dict()
    ret_dict.update(
            employee_code       =(lambda x: x['employee_code']      if x.has_key('employee_code')       else None)(args),
            jow_w_code          =(lambda x: x['jow_w_code']         if x.has_key('jow_w_code')          else None)(args),
            department_code     =(lambda x: x['department_code']    if x.has_key('department_code')     else None)(args),
            reason              =(lambda x: x['reason']             if x.has_key('reason')              else None)(args),
            note                =(lambda x: x['note']               if x.has_key('note')                else None)(args),
            first_name          =(lambda x: x['first_name']         if x.has_key('first_name')          else None)(args),
            last_name           =(lambda x: x['last_name']          if x.has_key('last_name')           else None)(args),
            job_w_name1         =(lambda x: x['job_w_name1']        if x.has_key('job_w_name1')         else None)(args),
            job_w_name2         =(lambda x: x['job_w_name2']        if x.has_key('job_w_name2')         else None)(args),
            department_name1    =(lambda x: x['department_name1']   if x.has_key('department_name1')    else None)(args),
            department_name2    =(lambda x: x['department_name2']   if x.has_key('department_name2')    else None)(args),
            created_on          =datetime.datetime.now(),
            created_by          =common.get_user_id(),
            modified_on         =None,
            modified_by         =''
            )
    return ret_dict

def update_emp_out(args, apr_period_emp_out):
    collection = common.get_collection('TMPER_AprPeriod')
    ret = collection.update(
        {
            "apr_period": args['data']['apr_period'],
            "apr_year": args['data']['apr_year'],
            "apr_period_emp_out": {
                "$elemMatch": {
                    "employee_code": args['data']["employee_code"]
                    }
                }
        },
        {
            "$set": {
                'apr_period_emp_out.$.employee_code': apr_period_emp_out['employee_code'],
                'apr_period_emp_out.$.jow_w_code': apr_period_emp_out['jow_w_code'],
                'apr_period_emp_out.$.department_code': apr_period_emp_out['department_code'],
                'apr_period_emp_out.$.reason': apr_period_emp_out['reason'],
                'apr_period_emp_out.$.note': apr_period_emp_out['note'],
                'apr_period_emp_out.$.first_name': apr_period_emp_out['first_name'],
                'apr_period_emp_out.$.last_name': apr_period_emp_out['last_name'],
                'apr_period_emp_out.$.job_w_name1': apr_period_emp_out['job_w_name1'],
                'apr_period_emp_out.$.job_w_name2': apr_period_emp_out['job_w_name2'],
                'apr_period_emp_out.$.department_name1': apr_period_emp_out['department_name1'],
                'apr_period_emp_out.$.department_name2': apr_period_emp_out['department_name2'],
                'apr_period_emp_out.$.modified_by': apr_period_emp_out['modified_by'],
                'apr_period_emp_out.$.modified_on': apr_period_emp_out['modified_on']
                }
        })
    return ret

def check_exist_apr_period_emp_out (args):
    ret = common.get_collection('TMPER_AprPeriod').find_one(
        {
            "apr_period": args['data']['apr_period'],
            "apr_year": args['data']['apr_year'],
            "apr_period_emp_out": {
                "$elemMatch": {
                    "employee_code": args['data']["employee_code"]
                }
            }
        })
    return ret

