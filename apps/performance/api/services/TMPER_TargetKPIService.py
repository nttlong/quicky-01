# -*- coding: utf-8 -*-
from .. import models
import qmongo
from qmongo import transaction
import datetime
from bson import ObjectId
from .. import common

def get_list_giao(args):
    searchText = args['data'].get('search', '')
    pageSize = args['data'].get('pageSize', 0)
    pageIndex = args['data'].get('pageIndex', 20)
    sort = args['data'].get('sort', 20)

    pageIndex = (lambda pIndex: pIndex if pIndex != None else 0)(pageIndex)
    pageSize = (lambda pSize: pSize if pSize != None else 20)(pageSize)
    search = (lambda x: x.strip() if searchText != None else "")(searchText)
    collection = qmongo.models.TMPER_TargetKPI.aggregate\
        .left_join(qmongo.models.HCSLS_Unit, "unit_code", "unit_code", "unit")\
        .project(
        rec_id = 1,
        apr_period=1,
        apr_year=1,
        employee_code=1,
        target_name=1,
        bsc_type=1,
        target=1,
        weight=1,
        baseline=1,
        min_value=1,
        max_value=1,
        modify_type=1,
        origin_target=1,
        unit_name= "unit.unit_name"
    ).match("apr_period == @period and apr_year == @year and employee_code == @emp_code",
            period = args['data']['apr_period'],
            year = args['data']['apr_year'],
            emp_code = args['data']['employee_code'])

    if (searchText != None):
        collection.match("contains(target_name, @name) or contains(unit_name, @name)" + \
                  " or contains(weight, @name) or contains(target, @name)" +\
                  " or contains(min_value, @name) or contains(max_value, @name)" + \
                  " or contains(origin_target, @name)", name=search.strip())

    if (sort != None):
        collection.sort(sort)

    return collection.get_page(pageIndex, pageSize)

def get(args):
    ret = None
    collection = models.TMPER_TargetKPI().aggregate()
    collection.left_join(models.auth_user_info(), "created_by", "username", "uc")
    collection.left_join(models.auth_user_info(), "modified_by", "username", "um")
    collection.project(
        rec_id=1,
        ref_id=1,
        apr_period=1,
        apr_year=1,
        employee_code=1,
        target_name=1,
        kpi_code=1,
        unit_code=1,
        cycle_type=1,
        target_desc=1,
        weight=1,
        kpi_formula=1,
        value_cal_type=1,
        parent_name=1,
        parent_code=1,
        bsc_type=1,
        begin_date=1,
        end_date=1,
        baseline=1,
        min_value=1,
        max_value=1,
        target=1,
        origin_target=1,
        perform=1,
        complete_pct=1,
        complete_date=1,
        modify_type=1,
        created_by="uc.login_account",
        created_on="created_on",
        modified_on="switch(case(modified_on!='',modified_on),'')",
        modified_by="switch(case(modified_by!='',um.login_account),'')"
    )
    collection.match("rec_id == @rec_id", rec_id = args['data']['rec_id'])

    ret = collection.get_item()

    return ret

def insert(args):
    ret = {}
    if(args['data']['status'] == 1):
        target_kpi_emp =qmongo.models.TMPER_TargetKPI_Emp.aggregate.project(
            rec_id = 1,
            apr_period = 1,
            apr_year = 1,
            employee_code = 1
        ).match("apr_period == @period and apr_year == @year and employee_code == @emp_code",
                period = args['data']['employee']['apr_period'],
                year = args['data']['employee']['apr_year'],
                emp_code = args['data']['employee']['employee_code']
                ).get_item()

        args['data']['entity'].update(
            ref_id = target_kpi_emp['rec_id']
        )
        ret = models.TMPER_TargetKPI().insert(args['data']['entity'])
        return ret
    elif(args['data']['status'] == 2):
        return ret.update(error = "data's waiting at portal")
    elif(args['data']['status'] == 3):
        #collection_TMPER_TargetKPI_Emp = models.TMPER_TargetKPI_Emp()
        #collection_TMPER_TargetKPI = models.TMPER_TargetKPI()

        # Tạo và start session
        #_session = transaction.create_session(collection_TMPER_TargetKPI_Emp)
        #transaction.start_transaction(_session)
        #try:

            #set session cho collection
            #collection_TMPER_TargetKPI_Emp.set_session(_session)
            #collection_TMPER_TargetKPI.set_session(_session)

            # import pymongo
            # from pymongo import MongoClient
            # client = MongoClient("172.16.7.67", 27017)

            # with client.start_session() as _session:
            #     _session.start_transaction()
            #
            #     db = client['lms']
            #
            #     db.get_collection('lv.TMPER_TargetKPI_Emp').insert(args['data']['employee'], _session)
            #     ret = db.get_collection('lv.TMPER_TargetKPI').insert(args['data']['entity'])
            #
            #     _session.commit_transaction()
            #
            #     return ret

            #Thao tác collection
    #         with qmongo.except_mode('on'):
    #             try:
    #                 args['data']['employee'].update(
    #                     assign_date= datetime.datetime.now(),
    #                     approver_code=common.get_employee_code(),
    #                     approver_date=datetime.datetime.now(),
    #                 )
    #                 emp = collection_TMPER_TargetKPI_Emp.insert(args['data']['employee'])
    #                 ret = collection_TMPER_TargetKPI.insert(args['data']['entity'])
    #             except Exception as ex:
    #                 raise ex
    #
    #     except Exception as ex:
    #         transaction.abort_transaction(_session)
    #         transaction.end_session(_session)
    #         raise ex
    #
    #     transaction.commit_transaction(_session)
    #     transaction.end_session(_session)
    #
    # return ret
        result_ins_emp = qmongo.models.TMPER_TargetKPI_Emp.insert(args['data']['employee'])
        if result_ins_emp.has_key('error') and result_ins_emp['error'] == None:
            try:
                args['data']['entity'].update(
                    ref_id = result_ins_emp['data']['rec_id']
                )
                ret = models.TMPER_TargetKPI().insert(args['data']['entity'])
                if ret.has_key('error') and ret['error'] != None:
                   qmongo.models.TMPER_TargetKPI_Emp.delete("_id == {0}", result_ins_emp['data']['_id'])
            except Exception as ex:
                qmongo.models.TMPER_TargetKPI_Emp.delete("_id == {0}", result_ins_emp['data']['_id'])
                raise ex

        return ret



def update(args):
    args['data']['entity'].update(
        employee_code = args['data']['employee']['employee_code']
    )
    ret = models.TMPER_TargetKPI().update(args['data']['entity'], "rec_id == @id", id = args['data']['entity']['rec_id'])
    return ret

def delete(args):
    ret = models.TMPER_TargetKPI().delete("rec_id in @id", id = [x["rec_id"] for x in args['data']])
    return ret

def get_target_kpi_by__apr_period_and_apr_year_and_emp_code(args):
    searchText = args['data'].get('search', '')
    pageSize = args['data'].get('pageSize', 0)
    pageIndex = args['data'].get('pageIndex', 20)
    sort = args['data'].get('sort', 20)

    pageIndex = (lambda pIndex: pIndex if pIndex != None else 0)(pageIndex)
    pageSize = (lambda pSize: pSize if pSize != None else 20)(pageSize)
    search = (lambda x: x.strip() if searchText != None else "")(searchText)

    ret = models.TMPER_TargetKPI().aggregate()\
        .project(
        target_name=1,
        weight=1,
        target=1,
        apr_period=1,
        apr_year=1,
        employee_code=1
        )\
        .match("apr_period == @period and apr_year == @year and employee_code == @code",
            period = args['data']['apr_period'],
            year = args['data']['apr_year'],
            code = args['data']['employee_code'])\

    if (search != None and search != ""):
        ret.match("contains(target_name, @name) or contains(weight, @name)" + \
                  " or contains(target, @name)", name=search.strip())

    if (sort != None):
        ret.sort(sort)

    return ret.get_page(pageIndex, pageSize)

def generate(args):
    try:
        db = common.get_db_context()
        # pGenDataCondition = {
        #     "opt_gen": 1,
        #     "apr_code": common.get_employee_code(),
        #     "apr_period": 2,
        #     "apr_year": 2018,
        #     "curr_apr_period": 1,
        #     "curr_apr_year": 2018,
        #     "is_copy_weight": True,
        #     "is_copy_target": True,
        #     "is_replace": True
        # }
        ret = db.system_js.TMPER_AprPeriod_FN_TMPER_TargetKPI_GenData(common.get_current_schema(),
                                                                      "PERF",
                                                                      common.get_user_id(),
                                                                      common.get_employee_code(),
                                                                      args['data']['selectedEmployee'],
                                                                      args['data']['selectedTarget'],
                                                                      args['data']['genGiveTargetCondition']
                                                                      )
        return ret
    except Exception as ex:
        raise ex

def get_list_update_target(args):
    searchText = args['data'].get('search', '')
    pageSize = args['data'].get('pageSize', 0)
    pageIndex = args['data'].get('pageIndex', 20)
    sort = args['data'].get('sort', 20)

    pageIndex = (lambda pIndex: pIndex if pIndex != None else 0)(pageIndex)
    pageSize = (lambda pSize: pSize if pSize != None else 20)(pageSize)
    search = (lambda x: x.strip() if searchText != None else "")(searchText)
    collection = models.TMPER_TargetKPI().aggregate() \
        .left_join(models.HCSLS_Unit(), "unit_code", "unit_code", "unit") \
        .project(
        rec_id=1,
        apr_period=1,
        apr_year=1,
        employee_code=1,
        target_name=1,
        kpi_code=1,
        bsc_type=1,
        target=1,
        baseline=1,
        min_value=1,
        max_value=1,
        modify_type=1,
        origin_target=1,
        perform=1,
        complete_pct=1,
        unit_name="unit.unit_name",
        weight=1,
    ).match("apr_period == @period and apr_year == @year and employee_code == @emp_code",
            period=args['data']['apr_period'],
            year=args['data']['apr_year'],
            emp_code=args['data']['employee_code'])

    if (searchText != None):
        collection.match("contains(target_name, @name) or contains(perform, @name)" + \
                         " or contains(weight, @name) or contains(target, @name)" + \
                         " or contains(min_value, @name) or contains(max_value, @name)" + \
                         " or contains(origin_target, @name)", name=search.strip())

    if (sort != None):
        collection.sort(sort)

    return collection.get_page(pageIndex, pageSize)

def get_list_update_target_by_id(args):
    ret = None
    collection = models.TMPER_TargetKPI().aggregate()
    collection.left_join(models.auth_user_info(), "created_by", "username", "uc")
    collection.left_join(models.auth_user_info(), "modified_by", "username", "um")
    collection.project(
        rec_id=1,
        ref_id=1,
        apr_period=1,
        apr_year=1,
        employee_code=1,
        target_name=1,
        kpi_code=1,
        unit_code=1,
        weight=1,
        parent_code=1,
        end_date=1,
        baseline=1,
        min_value=1,
        max_value=1,
        target=1,
        origin_target=1,
        perform=1,
        complete_pct=1,
        complete_date=1,
        modify_type=1,
        value_cal_type=1,
        kpi_formula=1,
        created_by="uc.login_account",
        created_on="created_on",
        modified_on="switch(case(modified_on!='',modified_on),'')",
        modified_by="switch(case(modified_by!='',um.login_account),'')"
    )
    collection.match("rec_id == @rec_id", rec_id = args['data']['rec_id'])

    ret = collection.get_item()

    return ret
