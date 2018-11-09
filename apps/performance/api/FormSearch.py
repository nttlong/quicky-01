# -*- coding: utf-8 -*-
import models
import common
import logging
import datetime
import threading
import quicky
import bson
logger = logging.getLogger(__name__)
import qmongo
def get_tree_kpi(args):
    ret=qmongo.models.TMLS_KPIGroup.aggregate.project(
        kpi_group_code = 1,
        kpi_group_name = 1,
        parent_code = 1,
        level = 1,
        level_code = 1,
        lock = 1
        ).match("lock != {0}", True)
        
    return ret.get_list()

#def get_list_kpi(args):
#    searchText = args['data'].get('search', '')
#    pageSize = args['data'].get('pageSize', 0)
#    pageIndex = args['data'].get('pageIndex', 20)
#    sort = args['data'].get('sort', 20)

#    pageIndex = (lambda pIndex: pIndex if pIndex != None else 0)(pageIndex)
#    pageSize = (lambda pSize: pSize if pSize != None else 20)(pageSize)

#    ret = models.TMLS_KPI().aggregate()
#    ret.left_join(models.SYS_VW_ValueList(), "cycle_type", "value", "val")
#    ret.match("val.list_name == {0}", "LCycleType")
#    ret.left_join(models.HCSLS_Unit(), "unit_code", "unit_code", "unit")
#    ret.project(
#        kpi_code      = "kpi_code",
#        kpi_name      = "kpi_name",
#        unit_code     = "unit.unit_name",
#        cycle_type    = "val.caption",
#        kpi_desc      = "kpi_desc",
#        weight        = "weight",
#        benchmark     = "benchmark",
#        is_apply_all  = "is_apply_all",
#        lock          = "lock"
#        )
#    ret.match("lock != {0}", True)

#    if(sort != None):
#        ret.sort(sort)
        
#    return ret.get_page(pageIndex, pageSize)

def get_list_kpi(args):
    searchText = args['data'].get('search', '')
    page_size = args['data'].get('pageSize', 0)
    page_index = args['data'].get('pageIndex', 20)
    sort = args['data'].get('sort', 20)

    collection = common.get_collection('TMLS_KPI')
    ret = collection.aggregate([
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
        'foreignField': 'kpi_group_code', 
        'as': 'kpig', 
        'from': common.get_collection_name_with_schema('TMLS_KPIGroup'), 
        'localField': 'kpi_group_code'
        }
    }, 
    {'$unwind': {
        'path': '$kpig', 
        'preserveNullAndEmptyArrays': True
        }
    }, 
    {'$project': {
        'kpi_name': '$kpi_name', 
        'is_apply_all': '$is_apply_all', 
        'kpi_desc': '$kpi_desc', 
        'cycle_type': { '$ifNull': [ '$val.caption', '' ] }, 
        'kpi_code': '$kpi_code', 
        'level_code': '$kpig.level_code',
        'weight': '$weight', 
        'unit_code': { '$ifNull': [ '$unit.unit_name', '' ] }, 
        'lock': '$lock', 
        'benchmark': { '$ifNull': [ '$benchmark', '' ] },
        'score_from': { '$ifNull': [ '$score_from', '' ] },
        'score_to': { '$ifNull': [ '$score_to', '' ] }
        }
    }, 
    {'$match': {'lock': {'$ne': True}, 'level_code':{'$eq':args['data']['kpi_group_code']}}}, 
    {'$sort': common.aggregate_sort(sort)},
    {"$facet": {
           "metadata": [{ "$count": "total" }, { "$addFields": { "page_index": page_index, "page_size": page_size } }],
           "data": [{ "$skip": page_size * page_index }, { "$limit": page_size }]
       }
    },
    {"$unwind": { "path": '$metadata', "preserveNullAndEmptyArrays": False }},
    {"$project": {
            'page_size': '$metadata.page_size',
            'page_index': '$metadata.page_index',
            'total_items': '$metadata.total',
            'items': '$data'
        }
    }])

    return (lambda x: x[0] if x != None and len(x) > 0 else {
        'page_size': page_size,
        'page_index': page_index,
        'total_items': 0,
        'items': []
        })(list(ret))

def get_list_employee_filter(args):
    try:
        ret = {}
        if args['data'] != None:
            searchText = args['data'].get('search', '')
            pageSize = args['data'].get('pageSize', 0)
            pageIndex = args['data'].get('pageIndex', 20)
            sort = args['data'].get('sort', 20)

            pageIndex = (lambda pIndex: pIndex if pIndex != None else 0)(pageIndex)
            pageSize = (lambda pSize: pSize if pSize != None else 20)(pageSize)

            if args['data'].has_key('where') and args['data']['where'].has_key('department_code'):
                ignore = args['data']['where']['ignore']
                return get_employee_list_by_department(args['data']['where']['department_code'], args['data']['where']['active'], pageSize, pageIndex, sort, (lambda x: x.strip() if x != None else "")(searchText), ignore)
            else:
                return dict(
                    error = "parameter 'department_code' is not exist"
                )

        return dict(
            error = "request parameter is not exist"
        )
    except Exception as ex:
        raise(ex)

def get_employee_list_by_department(dept_code, active, page_size, page_index, sort, search, ignore):
    if (active == "0"):
        active = {
            "$match":{"emp.active": {"$eq": True}}
            }
    elif (active == "1"):
        active = {
                "$match":{"emp.active": {"$ne": True}}
            }
    else:
        active =  {
            "$match":{"$or":[{"emp.active":{"$ne":True}}, {"emp.active":{"$eq":True}}]} #get all
            }

    rs = list(common.get_collection('SYS_ValueList').aggregate([{ "$match":  { "list_name": "LGender" } },
        { "$unwind": { "path": "$values", "preserveNullAndEmptyArrays": False } },
        { "$lookup": { "from": common.get_collection_name_with_schema("HCSEM_Employees"), "localField": "values.value", "foreignField": "gender", "as": "emp" } },
        { "$unwind": { "path": "$emp", "preserveNullAndEmptyArrays": True } },
        { "$lookup": { "from": common.get_collection_name_with_schema("HCSSYS_Departments"), "localField": "emp.department_code", "foreignField": "department_code", "as": "dept" } },
        { "$unwind": { "path": "$dept", "preserveNullAndEmptyArrays": False } },
        { "$match":  { "dept.level_code": dept_code } },
        active,
        { "$match":  { "emp.employee_code": { "$nin" : ignore }}},
        {
            "$project": {
                "full_name": { "$concat": ["$emp.last_name", " ", "$emp.first_name"] },
                "employee_code": "$emp.employee_code",
                "gender": "$values.caption",
                "job_w_code": "$emp.job_w_code",
                "join_date": "$emp.join_date",
                "department_code": "$emp.department_code",
                "department_name": "$dept.department_name",
                "photo_id": "$emp.photo_id",
                "last_name": "$emp.last_name",
                "first_name": "$emp.first_name",
                "extra_name": "$emp.extra_name",
                "birthday": "$emp.birthday",
                "b_province_code": "$emp.b_province_code",
                "nation_code": "$emp.nation_code",
                "ethnic_code": "$emp.ethnic_code",
                "religion_code": "$emp.religion_code",
                "culture_id": "$emp.culture_id",
                "is_retrain": "$emp.is_retrain",
                "train_level_code": "$emp.train_level_code",
                "marital_code": "$emp.marital_code",
                "id_card_no": "$emp.id_card_no",
                "issued_date": "$emp.issued_date",
                "issued_place_code": "$emp.issued_place_code",
                "mobile": "$emp.mobile",
                "p_phone": "$emp.p_phone",
                "email": "$emp.email",
                "personal_email": "$emp.personal_email",
                "document_no": "$emp.document_no",
                "official_date": "$emp.official_date",
                "career_date": "$emp.career_date",
                "personnel_date": "$emp.personnel_date",
                "emp_type_code": "$emp.emp_type_code",
                "labour_type": "$emp.labour_type",
                "job_pos_code": "$emp.job_pos_code",
                "job_pos_date": "$emp.job_pos_date",
                "job_w_date": "$emp.job_w_date",
                "profession_code": "$emp.profession_code",
                "level_management": "$emp.level_management",
                "is_cbcc": "$emp.is_cbcc",
                "is_expert_recruit": "$emp.is_expert_recruit",
                "is_expert_train": "$emp.is_expert_train",
                "manager_code": "$emp.manager_code",
                "manager_sub_code": "$emp.manager_sub_code",
                "user_id": "$emp.user_id",
                "job_pos_hold_code": "$emp.job_pos_hold_code",
                "job_w_hold_code": "$emp.job_w_hold_code",
                "department_code_hold": "$emp.department_code_hold",
                "job_pos_hold_from_date": "$emp.job_pos_hold_from_date",
                "job_pos_hold_to_date": "$emp.job_pos_hold_to_date",
                "end_date": "$emp.end_date",
                "retire_ref_no": "$emp.retire_ref_no",
                "signed_date": "$emp.signed_date",
                "signed_person": "$emp.signed_person",
                "active": "$emp.active",
                "note": "$emp.note",
                "p_address": "$emp.p_address",
                "p_province_code": "$emp.p_province_code",
                "p_district_code": "$emp.p_district_code",
                "p_ward_code": "$emp.p_ward_code",
                "p_hamlet_code": "$emp.p_hamlet_code",
                "t_address": "$emp.t_address",
                "t_province_code": "$emp.t_province_code",
                "t_district_code": "$emp.t_district_code",
                "t_ward_code": "$emp.t_ward_code",
                "t_hamlet_code": "$emp.t_hamlet_code",
                "foreigner": "$emp.foreigner",
                "vn_foreigner": "$emp.vn_foreigner",
                "is_not_reside": "$emp.is_not_reside",
                "fo_working": "$emp.fo_working",
                "fo_permiss": "$emp.fo_permiss",
                "fo_begin_date": "$emp.fo_begin_date",
                "fo_end_date": "$emp.fo_end_date"
            }
        },
        {
            "$match": {
                "$or": [{ "full_name": { "$regex": search, "$options": 'i' } },
                    { "employee_code": { "$regex": search, "$options": 'i' } },
                    { "gender": { "$regex": search, "$options": 'i' } },
                    { "job_w_code": { "$regex": search, "$options": 'i' } },
                    { "join_date": { "$regex": search, "$options": 'i' } },
                    { "department_name": { "$regex": search, "$options": 'i' } }]
            }
        },
        { "$sort": sort },
        {
            "$facet": {
                "metadata": [{ "$count": "total" }, { "$addFields": { "page_index": page_index, "page_size": page_size } }],
                "data": [{ "$skip": page_size * page_index }, { "$limit": page_size }]
            }
        },
        { "$unwind": { "path": '$metadata', "preserveNullAndEmptyArrays": False } },
        {
            "$project": {
                'page_size': '$metadata.page_size',
                'page_index': '$metadata.page_index',
                'total_items': '$metadata.total',
                'items': '$data',
            }
        }]))

    if len(rs) > 0:
        return rs[0]
    return {
        'page_size': page_size,
        'page_index': page_index,
        'total_items': 0,
        'items': [],
    }