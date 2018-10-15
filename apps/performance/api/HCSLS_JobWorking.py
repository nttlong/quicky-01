# -*- coding: utf-8 -*-
from bson import ObjectId
import models
from Query import JobWorking
import common
import logging
import datetime
import threading
logger = logging.getLogger(__name__)
global lock
from hcs_authorization import action_type,authorization
lock = threading.Lock()

@authorization.authorise(action=action_type.Action.READ)
def get_list_with_searchtext(args):
    if args['data'].has_key('gjw_code') and args['data']['gjw_code'] != None and args['data']['gjw_code'] != "":
        searchText = args['data'].get('search', '')
        pageSize = args['data'].get('pageSize', 0)
        pageIndex = args['data'].get('pageIndex', 20)
        sort = args['data'].get('sort', 20)

        pageIndex = (lambda pIndex: pIndex if pIndex != None else 0)(pageIndex)
        pageSize = (lambda pSize: pSize if pSize != None else 20)(pageSize)

        ret=JobWorking.display_list_job_working(args['data']['gjw_code'])

        ret=common.filter_lock(ret, args)
    
        if(searchText != None):
            ret.match("contains(job_w_name, @name) or contains(report_to_job_w, @name)" + \
                " or contains(job_w_code, @name) or contains(ordinal, @name)",name=searchText.strip())

        if(sort != None):
            ret.sort(sort)
        
        return ret.get_page(pageIndex, pageSize)
    return None

@authorization.authorise(action=action_type.Action.READ)
def get_job_working_group_by_group_code(args):
    try:
        if args['data'].has_key('gjw_code') and args['data']['gjw_code'] != None and args['data']['gjw_code'] != "":
            return JobWorking.get_job_working_group_by_group_code(args['data']['gjw_code'])
        return None
    except Exception as ex:
        raise ex

@authorization.authorise(action=action_type.Action.READ)
def get_list_permission_and_mission(args):
    searchText = args['data'].get('search', '')
    pageSize = args['data'].get('pageSize', 0)
    pageIndex = args['data'].get('pageIndex', 20)
    sort = args['data'].get('sort', 20)

    pageIndex = (lambda pIndex: pIndex if pIndex != None else 0)(pageIndex)
    pageSize = (lambda pSize: pSize if pSize != None else 20)(pageSize)

    ret = JobWorking.get_list_permission_and_mission_by_job_working_code(args['data']['job_w_code'],searchText)

    if(sort != None):
        ret.sort(sort)
        
    return ret.get_page(pageIndex, pageSize)

@authorization.authorise(action=action_type.Action.READ)
def get_job_description(args):
    try:
        if args['data'].has_key('job_w_code'):
            return JobWorking.get_job_description_by_job_working_code(args['data']['job_w_code']).get_item()

        return None
    except Exception as ex:
        raise ex

@authorization.authorise(action=action_type.Action.READ)
def get_list_evaluation_factor(args):
    try:
        searchText = args['data'].get('search', '')
        pageSize = args['data'].get('pageSize', 0)
        pageIndex = args['data'].get('pageIndex', 20)
        sort = args['data'].get('sort', 20)

        pageIndex = (lambda pIndex: pIndex if pIndex != None else 0)(pageIndex)
        pageSize = (lambda pSize: pSize if pSize != None else 20)(pageSize)
        if args['data'].has_key('job_w_code'):
            ret = JobWorking.get_list_evaluation_factor_by_job_working_code(args['data']['job_w_code'])
            if(sort != None):
                ret.sort(sort)
            return ret.get_page(pageIndex, pageSize)

        return None
    except Exception as ex:
        raise ex

@authorization.authorise(action=action_type.Action.CREATE)
def insert(args):
    try:
        lock.acquire()
        ret = {}
        if args['data'] != None:
            data =  set_dict_insert_data(args['data'])
            ret  =  models.HCSLS_JobWorking().insert(data)
            lock.release()
            ret['data'] = JobWorking.get_job_description_by_job_working_code(data['job_w_code']).get_item()
            return ret

        lock.release()
        return dict(
            error = "request parameter is not exist"
        )
    except Exception as ex:
        lock.release()
        raise(ex)

@authorization.authorise(action=action_type.Action.WRITE)
def update(args):
    try:
        lock.acquire()
        ret = {}
        if args['data'] != None:
            data =  set_dict_update_data(args['data'])
            ret  =  models.HCSLS_JobWorking().update(
                data, 
                "job_w_code == {0}", 
                args['data']['job_w_code'])
            if (ret.has_key('error') and ret['error'] == None) and ret['data'].raw_result['updatedExisting'] == True:
                ret.update(
                    data = get_job_description({"data":{"job_w_code":args['data']['job_w_code']}})
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

@authorization.authorise(action=action_type.Action.DELETE)
def delete(args):
    try:
        lock.acquire()
        ret = {}
        if args['data'] != None:
            #check HCSLS_JobWorking using by HCSEM_Employees
            list_code = [x["job_w_code"]for x in args['data']]
            list_employee = models.HCSEM_Employees().aggregate().project(job_w_code = 1).match("job_w_code in {0}", list_code).get_list()
            if len(list_employee) > 0:
                lock.release()
                return dict(
                    error = "JobWorking is using another PG",
                    items = list_employee
                )
            else:
                ret  =  models.HCSLS_JobWorking().delete("job_w_code in {0}", list_code)
                lock.release()
                return ret

        lock.release()
        return dict(
            error = "request parameter is not exist"
        )
    except Exception as ex:
        lock.release()
        raise(ex)

@authorization.authorise(action=action_type.Action.CREATE)
def insert_task(args):
    try:
        lock.acquire()
        ret = {}
        if args['data'] != None:
            if not args['data']['task'].has_key('rec_id'):
                if args['data'].has_key('job_w_code'):
                    task = set_dict_insert_task(args['data']['task'])
                    if(task.has_key('task_name')):
                        ret = JobWorking.insert_job_description(args, task)
                    else:
                        return dict(
                            error=dict(
                                fields=['task_name'],
                                code="missing"
                            )
                        )
                else:
                    lock.release()
                    return dict(
                        error = "request parameter job_w_code is not exist"
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

@authorization.authorise(action=action_type.Action.WRITE)
def update_task(args):
    try:
        lock.acquire()
        ret = {}
        if args['data'] != None:
            collection  =  common.get_collection('HCSLS_JobWorking')
            if args['data']['task'].has_key('rec_id'):
                check_exist = collection.find_one(
                    {
                        "job_w_code":args['data']['job_w_code'], 
                        "task":{
                                "$elemMatch":{
                                    "rec_id":args['data']['task']["rec_id"]
                                    }
                             }
                     })
                if check_exist != None:
                    task = set_dict_update_task(args['data']['task'])
                    if(task.has_key('task_name')):
                        ret = JobWorking.update_job_description(args, task)
                    else:
                        return dict(
                            error=dict(
                                fields=['task_name'],
                                code="missing"
                            )
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

@authorization.authorise(action=action_type.Action.DELETE)
def delete_task(args):
    try:
        lock.acquire()
        ret = {}
        error_message = None
        if args['data'] != None:
            if args['data'].has_key('job_w_code'):
                if args['data'].has_key('rec_id'):
                    ret = JobWorking.remove_job_description(args)
                    lock.release()
                    return ret
                else:
                    error_message = "parameter 'rec_id' is not exist"
            else:
                error_message = "parameter 'job_w_code' is not exist"

            lock.release()
            return dict(
                error = error_message
            )
        else:
            error_message = "request parameter is not exist"

        lock.release()
        return dict(
            error = error_message
        )
    except Exception as ex:
        lock.release()
        raise(ex)

@authorization.authorise(common=True)
def set_dict_insert_data(args):
    ret_dict = dict()

    ret_dict.update(
        job_w_code           = (lambda x: x['job_w_code']          if x.has_key('job_w_code')           else None)(args),
        job_w_name           = (lambda x: x['job_w_name']          if x.has_key('job_w_name')           else None)(args),
        job_w_name2          = (lambda x: x['job_w_name2']         if x.has_key('job_w_name2')          else None)(args),
        job_w_duty           = (lambda x: x['job_w_duty']          if x.has_key('job_w_duty')           else None)(args),
        gjw_code             = (lambda x: x['gjw_code']            if x.has_key('gjw_code')             else None)(args),
        ordinal              = (lambda x: x['ordinal']             if x.has_key('ordinal')              else None)(args),
        lock                 = (lambda x: x['lock']                if x.has_key('lock')                 else None)(args),
        is_job_w_main_staff  = (lambda x: x['is_job_w_main_staff'] if x.has_key('is_job_w_main_staff')  else None)(args),
        report_to_job_w      = (lambda x: x['report_to_job_w']     if x.has_key('report_to_job_w')      else None)(args),
        internal_process     = (lambda x: x['internal_process']    if x.has_key('internal_process')     else None)(args),
        combine_process      = (lambda x: x['combine_process']     if x.has_key('combine_process')      else None)(args),
        description          = (lambda x: x['description']         if x.has_key('description')          else None)(args),
        effect_date          = (lambda x: x['effect_date']         if x.has_key('effect_date')          else None)(args),
        job_pos_code         = (lambda x: x['job_pos_code']        if x.has_key('job_pos_code')         else None)(args),
        dept_apply           = (lambda x: x['dept_apply']          if x.has_key('dept_apply')           else [])(args),
        dept_contact         = (lambda x: x['dept_contact']        if x.has_key('dept_contact')         else [])(args),
        job_w_next           = (lambda x: x['job_w_next']          if x.has_key('job_w_next')           else [])(args),
        job_w_change         = (lambda x: x['job_w_change']        if x.has_key('job_w_change')         else [])(args),
        task                 = (lambda x: x['task']                if x.has_key('task')                 else [])(args),
        factor_appraisal     = (lambda x: x['factor_appraisal']    if x.has_key('factor_appraisal')     else [])(args),
        kpi                  = (lambda x: x['kpi']                 if x.has_key('kpi')                  else [])(args)
    )

    return ret_dict

@authorization.authorise(common=True)
def set_dict_update_data(args):
    ret_dict = set_dict_insert_data(args)
    del ret_dict['job_w_code']
    del ret_dict['task']
    del ret_dict['factor_appraisal']
    del ret_dict['kpi']
    return ret_dict

@authorization.authorise(common=True)
def set_dict_insert_task(args):
    ret_dict = dict()
    ret_dict.update(
            rec_id            = common.generate_guid(),
            task_name         = (lambda x: x['task_name']      if x.has_key('task_name')       else None)(args),
            weight            = (lambda x: x['weight']         if x.has_key('weight')          else None)(args),
            description       = (lambda x: x['description']    if x.has_key('description')     else None)(args),
            ordinal           = (lambda x: x['ordinal']        if x.has_key('ordinal')         else None)(args),
            created_on        = datetime.datetime.now(),
            created_by        = common.get_user_id(),
            modified_on       = None,
            modified_by       = ''
            )
    return ret_dict

@authorization.authorise(common=True)
def set_dict_update_task(args):
    ret_dict = set_dict_insert_task(args)
    del ret_dict['rec_id']
    ret_dict['modified_on'] = datetime.datetime.now()
    ret_dict['modified_by'] = common.get_user_id()
    return ret_dict

@authorization.authorise(action=action_type.Action.READ)
def get_list_performance_standanrd(args):
    searchText = args['data'].get('search', '')
    pageSize = args['data'].get('pageSize', 0)
    pageIndex = args['data'].get('pageIndex', 20)
    sort = args['data'].get('sort', 20)

    pageIndex = (lambda pIndex: pIndex if pIndex != None else 0)(pageIndex)
    pageSize = (lambda pSize: pSize if pSize != None else 20)(pageSize)

    ret = get_list_performance_standanrd_by_job_working_code(args['data']['job_w_code'])

    if(sort != None):
        ret.sort(sort)
        
    return ret.get_page(pageIndex, pageSize)

@authorization.authorise(action=action_type.Action.READ)
def get_list_performance_standanrd_by_job_working_code(job_w_code):
    ret=models.HCSLS_JobWorking().aggregate()
    ret.match("job_w_code == {0}", job_w_code)
    ret.unwind("kpi")
    ret.left_join(models.auth_user_info(), "created_by", "username", "uc")
    ret.left_join(models.auth_user_info(), "modified_by", "username", "um")
    ret.project(
        job_w_code="job_w_code",
        rec_id ="kpi.rec_id",
        #kpi_code="kpi.kpi_code",
        kpi_name="kpi.kpi_name",
        weight="kpi.weight",
        unit="kpi.unit",
        scope_from = "kpi.score_from",
        scope_to = "kpi.scope_to",
        cycle="kpi.cycle",
        ordinal="kpi.ordinal",
        created_by="uc.login_account",
        created_on="kpi.created_on",
        modified_on="switch(case(kpi.modified_on!='',kpi.modified_on),'')",
        modified_by="switch(case(kpi.modified_by!='',um.login_account),'')",
    )
    ret.match("kpi_name != {0}", None)
    ret.sort(dict(
        ordinal = 1
    ))

    return ret

@authorization.authorise(action=action_type.Action.CREATE)
def insert_kpi(args):
    try:
        lock.acquire()
        ret = {}
        if args['data'] != None:
            if not args['data']['kpi'].has_key('rec_id'):
                if args['data'].has_key('job_w_code'):
                    kpi = set_dict_insert_kpi(args['data']['kpi'])
                    if(kpi.has_key('task_name')):
                        ret = JobWorking.insert_kpi(args, kpi)
                    else:
                        return dict(
                            error=dict(
                                fields=['task_name'],
                                code="missing"
                            )
                        )
                else:
                    lock.release()
                    return dict(
                        error = "request parameter job_w_code is not exist"
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

@authorization.authorise(common = True)
def set_dict_insert_kpi(args):
    ret_dict = dict()
    ret_dict.update(
            rec_id            = common.generate_guid(),
            kpi_name          = (lambda x: x['kpi_name']      if x.has_key('kpi_name')       else None)(args),
            unit              = (lambda x: x['unit']         if x.has_key('unit')          else None)(args),
            cycle              = (lambda x: x['cycle']         if x.has_key('cycle')          else None)(args),
            weight            = (lambda x: x['weight']         if x.has_key('weight')          else None)(args),
            description       = (lambda x: x['description']    if x.has_key('description')     else None)(args),
            ordinal           = (lambda x: x['ordinal']        if x.has_key('ordinal')         else None)(args),
            created_on        = datetime.datetime.now(),
            created_by        = common.get_user_id(),
            modified_on       = None,
            modified_by       = ''
            )
    return ret_dict

@authorization.authorise(action=action_type.Action.WRITE)
def update_kpi(args):
    try:
        lock.acquire()
        ret = {}
        if args['data'] != None:
            collection  =  common.get_collection('HCSLS_JobWorking')
            if args['data']['kpi'].has_key('rec_id'):
                check_exist = collection.find_one(
                    {
                        "job_w_code":args['data']['job_w_code'], 
                        "kpi":{
                                "$elemMatch":{
                                    "rec_id":args['data']['kpi']["rec_id"]
                                    }
                             }
                     })
                if check_exist != None:
                    kpi = set_dict_update_kpi(args['data']['kpi'])
                    ret = JobWorking.update_job_kpi(args, kpi)

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
def delete_kpi(args):
    try:
        lock.acquire()
        ret = {}
        error_message = None
        if args['data'] != None:
            if args['data'].has_key('job_w_code'):
                if args['data'].has_key('rec_id'):
                    ret = JobWorking.remove_kpi(args)
                    lock.release()
                    return ret
                else:
                    error_message = "parameter 'rec_id' is not exist"
            else:
                error_message = "parameter 'job_w_code' is not exist"

            lock.release()
            return dict(
                error = error_message
            )
        else:
            error_message = "request parameter is not exist"

        lock.release()
        return dict(
            error = error_message
        )
    except Exception as ex:
        lock.release()
        raise(ex)

@authorization.authorise(common=True)
def set_dict_update_kpi(args):
    ret_dict = set_dict_insert_kpi(args)
    del ret_dict['rec_id']
    ret_dict['modified_on'] = datetime.datetime.now()
    ret_dict['modified_by'] = common.get_user_id()
    return ret_dict

@authorization.authorise(action=action_type.Action.CREATE)
def insert_factor_appraisal(args):
    try:
        lock.acquire()
        ret = {}
        if args['data'] != None:
            if not args['data']['factor_appraisal'].has_key('rec_id'):
                if args['data'].has_key('job_w_code'):
                    if(args['data']['factor_appraisal'].has_key('factor_code')):
                        for x in args['data']['factor_appraisal']['factor_code']:
                            try:
                                param = {
                                    "job_w_code":args['data']['job_w_code'],
                                    "factor_code":str(x).format(),
                                    "weight":(lambda x: x['weight'] if x.has_key('weight') else None)(args['data']['factor_appraisal']),
                                    }
                                factor = set_dict_insert_factor_appraisal(param)
                                ret = JobWorking.insert_evaluation_factor(args, factor)
                            except Exception as ex:
                                raise ex
                    else:
                        return dict(
                            error=dict(
                                fields=['factor_code'],
                                code="missing"
                            )
                        )
                else:
                    lock.release()
                    return dict(
                        error=dict(
                                fields=['factor_code'],
                                code="missing"
                            )
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

@authorization.authorise(action=action_type.Action.WRITE)
def update_factor_appraisal(args):
    try:
        lock.acquire()
        ret = {}
        if args['data'] != None:
            collection  =  common.get_collection('HCSLS_JobWorking')
            if args['data']['factor_appraisal'].has_key('rec_id'):
                check_exist = collection.find_one(
                    {
                        "job_w_code":args['data']['job_w_code'], 
                        "factor_appraisal":{
                                "$elemMatch":{
                                    "rec_id":args['data']['factor_appraisal']["rec_id"]
                                    }
                             }
                     })
                if check_exist != None:
                    factor = set_dict_update_factor_appraisal(args['data']['factor_appraisal'])
                    if(factor.has_key('factor_code')):
                        ret = JobWorking.update_evaluation_factor(args, factor)
                    else:
                        return dict(
                            error=dict(
                                fields=['factor_code'],
                                code="missing"
                            )
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

@authorization.authorise(action=action_type.Action.DELETE)
def delete_factor_appraisal(args):
    try:
        lock.acquire()
        ret = {}
        error_message = None
        if args['data'] != None:
            if args['data'].has_key('job_w_code'):
                if args['data'].has_key('rec_id'):
                    ret = JobWorking.delete_evaluation_factor(args)
                    lock.release()
                    return ret
                else:
                    error_message = "parameter 'rec_id' is not exist"
            else:
                error_message = "parameter 'job_w_code' is not exist"

            lock.release()
            return dict(
                error = error_message
            )
        else:
            error_message = "request parameter is not exist"

        lock.release()
        return dict(
            error = error_message
        )
    except Exception as ex:
        lock.release()
        raise(ex)

@authorization.authorise(common = True)
def set_dict_insert_factor_appraisal(args):
    ret_dict = dict()
    ret_dict.update(
            rec_id            = common.generate_guid(),
            jow_w_code        = (lambda x: x['jow_w_code']      if x.has_key('jow_w_code')      else None)(args),
            factor_code       = (lambda x: x['factor_code']     if x.has_key('factor_code')     else None)(args),
            weight            = (lambda x: x['weight']          if x.has_key('weight')          else None)(args),
            created_on        = datetime.datetime.now(),
            created_by        = common.get_user_id(),
            modified_on       = None,
            modified_by       = ''
            )
    return ret_dict

@authorization.authorise(common = True)
def set_dict_update_factor_appraisal(args):
    ret_dict = set_dict_insert_factor_appraisal(args)
    del ret_dict['rec_id']
    ret_dict['modified_on'] = datetime.datetime.now()
    ret_dict['modified_by'] = common.get_user_id()
    return ret_dict

@authorization.authorise(action=action_type.Action.READ)
def get_list_performance_standanrd(args):
    try:
        search = args['data'].get('search', '')
        if search == None:
            search = ""
        page_size = args['data'].get('pageSize', 0)
        page_index = args['data'].get('pageIndex', 20)
        sort = args['data'].get('sort', 20)
        collection = common.get_collection('HCSLS_JobWorking')
        ret = collection.aggregate([
        {'$unwind': {
            'path': '$kpi', 
            'preserveNullAndEmptyArrays': False
            }
        },
        {'$project': {
            'job_w_code': '$job_w_code',
            'rec_id':'$kpi.rec_id',
            'kpi_code': '$kpi.kpi_code', 
            'cycle_type': "$kpi.cycle", 
            'weight': '$kpi.weight', 
            'unit_code': "$kpi.unit", 
            'description': '$kpi.description',
            #'standard_mark': '$kpi.standard_mark', 
            'score_from': '$kpi.score_from',
            'score_to': '$kpi.score_to',
            'note': "$kpi.note",
            'created_by': '$kpi.created_by', 
            'created_on': "$kpi.created_on", 
            'modified_by': '$kpi.modified_by', 
            'modified_on': "$kpi.modified_on"
            }
        },
        {'$lookup': {
            'foreignField': 'value', 
            'as': 'val', 
            'from': common.get_collection_name_with_schema('SYS_VW_ValueList'),
            'localField': 'cycle_type'
            }
        }, 
        {'$unwind': {
            'path': '$val', 
            'preserveNullAndEmptyArrays': True
            }
        }, 
        {'$lookup': {
            'foreignField': 'username', 
            'as': 'uc', 
            'from': common.get_collection_name_with_schema('auth_user_info'),
            'localField': 'created_by'
            }
        }, 
        {'$unwind': {
            'path': '$uc', 
            'preserveNullAndEmptyArrays': True
            }
        }, 
        {'$lookup': {
            'foreignField': 'username', 
            'as': 'um', 
            'from': common.get_collection_name_with_schema('auth_user_info'),
            'localField': 'modified_by'
            }
        }, 
        {'$unwind': {
            'path': '$um', 
            'preserveNullAndEmptyArrays': True
            }
        }, 
        {'$match': {   
            '$and':[{
                        '$or' :[{ 'val.list_name':None},
                                { 'val.list_name':'LCycleType'}]
                    },
                    {
                        '$or' :[{ 'val.language':None},
                                { 'val.language': common.get_language()}]
                    }]
            }
        },
        {'$lookup': {
            'foreignField': 'unit_code', 
            'as': 'unit', 
            'from': common.get_collection_name_with_schema('HCSLS_Unit'), 
            'localField': 'unit_code'
            }
        }, 
        {'$unwind': {
            'path': '$unit', 
            'preserveNullAndEmptyArrays': True
            }
        }, 
        {'$lookup': {
            'foreignField': 'kpi_code', 
            'as': 'h_kpi', 
            'from': common.get_collection_name_with_schema('TMLS_KPI'), 
            'localField': 'kpi_code'
            }
        }, 
        {'$unwind': {
            'path': '$h_kpi', 
            'preserveNullAndEmptyArrays': True
            }
        }, 
        {'$project': {
            'job_w_code':'$job_w_code',
            'rec_id':'$rec_id',
            'kpi_name': '$h_kpi.kpi_name', 
            'kpi_desc': { '$ifNull': [ '$h_kpi.kpi_desc', '' ] }, 
            'cycle_type': { '$ifNull': [ '$val.caption', '' ] }, 
            'cycle' : '$cycle_type',
            'kpi_code': { '$ifNull': [ '$kpi_code', '' ] }, 
            'weight': '$weight', 
            'unit': { '$ifNull': [ '$unit.unit_name', '' ] }, 
            'unit_code' : '$unit',
            'description': "$h_kpi.kpi_desc",
            #'standard_mark': "$standard_mark",
            'score_from': "$score_from",
            'score_to': "$score_to",
            'note':'$note',
            'created_by': { '$ifNull': [ '$uc.login_account', '' ] }, 
            'created_on': "$created_on", 
            'modified_by': { '$ifNull': [ '$um.login_account', '' ] }, 
            'modified_on': "$modified_on"
            }
        },
        { '$match': {
                "$and":[{
                    "$or": [{ "kpi_name": { "$regex": search, "$options": 'i' } },
                            { "unit_code": { "$regex": search, "$options": 'i' } },
                            { "cycle_type": { "$regex": search, "$options": 'i' } },
                            { "note": { "$regex": search, "$options": 'i' } },
                            { "description": { "$regex": search, "$options": 'i' } },
                            #{ "standard_mark": { "$regex": search, "$options": 'i' } },
                            { "score_from": { "$regex": search, "$options": 'i' } },
                            { "score_to": { "$regex": search, "$options": 'i' } }]
                    },{
                        "job_w_code":args['data']['job_w_code']
                    }]
            }
        },
        { "$sort": common.aggregate_sort(sort) },
            {
            "$facet": {
                "metadata": [{ "$count": "total" }, { "$addFields": { "page_index": page_index, "page_size": page_size } }],
                "data": [{ "$skip": page_size * page_index }, { "$limit": page_size }]
            }
        },
        { 
            "$unwind": { "path": '$metadata', "preserveNullAndEmptyArrays": False } 
        },
        {
            "$project": {
                'page_size': '$metadata.page_size',
                'page_index': '$metadata.page_index',
                'total_items': '$metadata.total',
                'items': '$data'
            }
        }
        ])

        return (lambda x: x[0] if x != None and len(x) > 0 else {
            "page_size":"",
            "page_index":"",
            "total_items":0,
            "items":[],
            })(list(ret))
    except Exception as ex:
        raise(ex)

@authorization.authorise(action=action_type.Action.CREATE)
def insert_performance_standanrd(args):
    try:
        lock.acquire()
        #Trường hợp chọn 1
        if len(args['data']['kpi']['kpi_code']) == 1:
            data = dict_insert_performance_standanrd(args['data']['kpi'])
            import TMLS_KPI
            #if (data['weight'] == None or data['weight'] == "") or (data['standard_mark'] == None or data['standard_mark'] == ""):
            #default = TMLS_KPI.get_kpi_by_kpi_code({"data":{"kpi_code":args['data']['kpi']['kpi_code'][0]}})
            default = models.TMLS_KPI().aggregate().project(
                kpi_code = 1,
                kpi_group_code = 1,
                unit_code = 1,
                cycle_type = 1,
                kpi_desc = 1,
                weight = 1,
                benchmark = 1,
                score_from = 1,
                score_to = 1
                ).match("kpi_code == {0}", args['data']['kpi']['kpi_code'][0]).get_item()
            data['description'] = default['kpi_desc']
            data['unit'] = default['unit_code']
            data['cycle'] = default['cycle_type']
            data['kpi_code'] = data['kpi_code'][0]
            #default nếu bỏ trống
            data['weight'] = (lambda x, y: x if y == None or y == "" else y)(default['weight'], args['data']['kpi']['weight'])
            #default nếu bỏ trống
            #data['standard_mark'] = (lambda x, y: x if y == None or y == "" else y)(default['benchmark'], args['data']['kpi']['standard_mark'])
            data['score_from'] = (lambda x, y: x if y == None or y == "" else y)(default['benchmark'], args['data']['kpi']['score_from'])
            data['score_to'] = (lambda x, y: x if y == None or y == "" else y)(default['benchmark'], args['data']['kpi']['score_to'])
            collection  =  common.get_collection('HCSLS_JobWorking')
            check_exist = collection.find_one(
                            {
                                "job_w_code":args['data']['job_w_code'], 
                                "kpi":{
                                        "$elemMatch":{
                                            "kpi_code":args['data']['kpi']['kpi_code']
                                            }
                                        }
                                })
            ret = None
            if check_exist != None:
                ret = {
                    "error" : "duplicate",
                    "item" : check_exist
                }
                lock.release()
                return ret
            try:
                ret = collection.update({ "job_w_code": args['data']['job_w_code'] },
                                        {
                                        '$push': {
                                            "kpi": data
                                        }
                                        }
                                    )
                ret.update(error=None)
                lock.release()
                return ret
            except Exception as ex:
                lock.release()
                return {
                    "error": ex.message
                    }
        elif len(args['data']['kpi']['kpi_code']) > 1:
            #Trường hợp chọn nhiều

            #check duplicate
            collection  =  common.get_collection('HCSLS_JobWorking')
            check_exist = collection.find(
                                {
                                    "job_w_code":args['data']['job_w_code'], 
                                    "kpi":{
                                            "$elemMatch":{
                                                "kpi_code": {'$in': args['data']['kpi']['kpi_code']}
                                                }
                                            }
                                    })
            ret = None
            rs_check = list(check_exist)
            if len(rs_check) > 0:
                ret = {
                    "error" : "duplicate",
                    "item" : rs_check
                }
                lock.release()
                return ret

            data = []
            for x in args['data']['kpi']['kpi_code']:
                tmp = dict_insert_performance_standanrd(args['data']['kpi'])
                tmp['kpi_code'] = x
                default = models.TMLS_KPI().aggregate().project(
                    kpi_code = 1,
                    kpi_group_code = 1,
                    unit_code = 1,
                    cycle_type = 1,
                    kpi_desc = 1,
                    weight = 1,
                    benchmark = 1
                    ).match("kpi_code == {0}", x).get_item()
                tmp['description'] = default['kpi_desc']
                tmp['unit'] = default['unit_code']
                tmp['cycle'] = default['cycle_type']
                if args['data']['kpi']['weight'] == None or args['data']['kpi']['weight'] == "":
                    tmp['weight'] = default['weight']
                else:
                    tmp['weight'] = args['data']['kpi']['weight']

                #if args['data']['kpi']['standard_mark'] == None or args['data']['kpi']['standard_mark'] == "":
                #    tmp['standard_mark'] = default['benchmark']
                #else:
                #    tmp['standard_mark'] = args['data']['kpi']['standard_mark']

                if args['data']['kpi']['score_from'] == None or args['data']['kpi']['score_from'] == "":
                    tmp['score_from'] = default['score_from']
                else:
                    tmp['score_from'] = args['data']['kpi']['score_from']

                if args['data']['kpi']['score_to'] == None or args['data']['kpi']['score_to'] == "":
                    tmp['score_to'] = default['score_to']
                else:
                    tmp['score_to'] = args['data']['kpi']['score_to']

                data.append(tmp)
            try:
                for x in data:
                    ret = collection.update({ "job_w_code": args['data']['job_w_code'] },
                                              {
                                                '$push': {
                                                  "kpi": x
                                                }
                                              }
                                            )

                ret.update(error=None)
                lock.release()
                return ret
            except Exception as ex:
                lock.release()
                return {
                        "error": ex.message
                        }
        else:
            #Trường hợp rỗng
            lock.release()
            return {
                    "error": "missing",
                    "fields":["kpi_code"]
                    }

    except Exception as ex:
        lock.release()
        raise(ex)

@authorization.authorise(common = True)
def dict_insert_performance_standanrd(args):
    ret = dict()
    ret.update(
        rec_id = common.generate_guid(),
        kpi_code =      (lambda x: x['kpi_code']        if x.has_key('kpi_code')      else None)(args),
        kpi_name =      (lambda x: x['kpi_name']        if x.has_key('kpi_name')      else None)(args),
        unit =          (lambda x: x['unit']            if x.has_key('unit')          else None)(args),
        description =   (lambda x: x['description']     if x.has_key('description')   else None)(args),
        cycle =         (lambda x: x['cycle']           if x.has_key('cycle')         else None)(args),
        weight =        (lambda x: x['weight']          if x.has_key('weight')        else None)(args),
        #standard_mark = (lambda x: x['standard_mark']   if x.has_key('standard_mark') else None)(args),
        score_from =    (lambda x: x['score_from']      if x.has_key('score_from')    else None)(args),
        score_to =      (lambda x: x['score_to']        if x.has_key('score_to')      else None)(args),
        note =          (lambda x: x['note']            if x.has_key('note')          else None)(args),
        created_on = datetime.datetime.now(),
        created_by = common.get_user_id(),
        modified_on = "",
        modified_by = ""
        )
    return ret

@authorization.authorise(action=action_type.Action.WRITE)
def update_performance_standanrd(args):
    try:
        lock.acquire()
        data = dict_insert_performance_standanrd(args['data']['kpi'])
        import TMLS_KPI
        default = models.TMLS_KPI().aggregate().project(
            kpi_code = 1,
            kpi_group_code = 1,
            unit_code = 1,
            cycle_type = 1,
            kpi_desc = 1,
            weight = 1,
            benchmark = 1,
            score_from = 1,
            score_to = 1
            ).match("kpi_code == {0}", args['data']['kpi']['kpi_code']).get_item()
        data['description'] = default['kpi_desc']
        data['unit'] = default['unit_code']
        data['cycle'] = default['cycle_type']
        data['kpi_code'] = data['kpi_code']
        #default nếu bỏ trống
        data['weight'] = (lambda x, y: x if y == None or y == "" else y)(default['weight'], args['data']['kpi']['weight'])
        #default nếu bỏ trống
        #data['standard_mark'] = (lambda x, y: x if y == None or y == "" else y)(default['benchmark'], args['data']['kpi']['standard_mark'])
        data['score_from'] = (lambda x, y: x if y == None or y == "" else y)(default['score_from'], args['data']['kpi']['score_from'])
        data['score_to'] = (lambda x, y: x if y == None or y == "" else y)(default['score_to'], args['data']['kpi']['score_to'])
        collection  =  common.get_collection('HCSLS_JobWorking')
        check_exist = collection.find(
                        {
                            "job_w_code":args['data']['job_w_code'], 
                            "kpi":{
                                    "$elemMatch":{
                                        "kpi_code":args['data']['kpi']['kpi_code']
                                        }
                                    }
                            })
        ret = None
        list_check = list(check_exist)
        if list_check != None and len(list_check) > 1:
            ret = {
                "error" : "duplicate",
                "item" : check_exist
            }
            lock.release()
            return ret
        try:
            ret = collection.update({
                        "job_w_code": args['data']['job_w_code'],
                        "kpi":{
                            "$elemMatch":{
                                "rec_id":args['data']['kpi']["rec_id"]
                                }
                            }
                        },
                        {
                            "$set": {
                                'kpi.$.kpi_code': data['kpi_code'],
                                'kpi.$.weight': data['weight'],
                                #'kpi.$.standard_mark': data['standard_mark'],
                                'kpi.$.score_from': data['score_from'],
                                'kpi.$.score_to': data['score_to'],
                                'kpi.$.note': data['note'],
                                'kpi.$.modified_by': common.get_user_id(),
                                'kpi.$.modified_on': datetime.datetime.now(),
                                'kpi.$.description': data['description'],
                                'kpi.$.unit': data['unit'],
                                'kpi.$.cycle': data['cycle']
                                }
                        })
            ret.update(error=None)
            lock.release()
            return ret
        except Exception as ex:
            lock.release()
            return {
                "error": ex.message
                }
    except Exception as ex:
        lock.release()
        raise(ex)

@authorization.authorise(action=action_type.Action.DELETE)
def delete_performance_standard(args):
    try:
        lock.acquire()
        ret = {}
        error_message = None
        if args['data'] != None:
            if args['data'].has_key('job_w_code'):
                if args['data'].has_key('rec_id'):
                    collection  =  common.get_collection('HCSLS_JobWorking')
                    ret = collection.update(
                        {
                            "job_w_code": args['data']['job_w_code']
                        },
                        {
                            '$pull':{"kpi" :{ "rec_id": {'$in': args['data']['rec_id']}}}
                        }, 
                        True
                        )
                    lock.release()
                    return ret
                else:
                    error_message = "parameter 'rec_id' is not exist"
            else:
                error_message = "parameter 'job_w_code' is not exist"

            lock.release()
            return dict(
                error = error_message
            )
        else:
            error_message = "request parameter is not exist"

        lock.release()
        return dict(
            error = error_message
        )
    except Exception as ex:
        lock.release()
        raise(ex)