from .. import models
from .. import common
def get_employee_list_by_department(dept_code, page_size, page_index, sort, search):
    db = common.get_db_context()
    ret = db.system_js.getEmployeeByDepartmentCode(common.get_current_schema(), "PERF", dept_code, page_size, page_index, sort, search)
    return ret

def get_empworking_by_employee_code(emp_code, page_index, page_size, sort, search):
    ret = {}
    collection = common.get_collection('HCSEM_EmpWorking').aggregate([{"$match":{'employee_code':{'$regex':'^' + emp_code}}},
        {"$lookup":{'from':common.get_collection_name_with_schema('HCSSYS_Departments'), 'localField':'department_code', 'foreignField':'department_code', 'as': 'dept'}},
        {"$unwind":{'path':'$dept', "preserveNullAndEmptyArrays":True}},
        {"$lookup":{'from':common.get_collection_name_with_schema('HCSLS_Position'), 'localField':'job_pos_code', 'foreignField':'job_pos_code', 'as': 'job_pos'}},
        {"$unwind":{'path':'$job_pos', "preserveNullAndEmptyArrays":True}},
        {"$lookup":{'from':common.get_collection_name_with_schema('HCSLS_JobWorking'), 'localField':'job_w_code', 'foreignField':'job_w_code', 'as': 'job_w'}},
        {"$unwind":{'path':'$job_w', "preserveNullAndEmptyArrays":True}},
        {"$project":{
            "employee_code"             : 1,
            "appoint"                   : 1,
            "effect_date"               : 1,
            "begin_date"                : 1,
            "end_date"                  : 1,
            "decision_no"               : 1,
            "signed_date"               : 1,
            "signer_code"               : 1,
            "note"                      : 1,
            "task"                      : 1,
            "reason"                    : 1,
            "department_code"           : 1,
            "job_pos_code"              : 1,
            "job_w_code"                : 1,
            "emp_type_code"             : 1,
            "region_code"               : 1,
            "department_code_old"       : 1,
            "job_pos_code_old"          : 1,
            "job_w_code_old"            : 1,
            "emp_type_code_old"         : 1,
            "region_code_old"           : 1,
            "province_code"             : 1,
            "department_name"           : { "$ifNull": [ "$dept.department_name", "" ] },
            "job_pos_name"              : { "$ifNull": [ "$job_pos.job_pos_name", "" ] },
            "job_w_name"                : { "$ifNull": [ "$job_w.job_w_name", "" ] },
            "region_name"               : { "$ifNull": [ "$job_w.region_name", "" ] }

         }},
         { "$sort": sort },
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
        }])

    #if len(list(collection)) > 0:
    ret = list(collection)
    #else:
    #    ret = {
    #        'page_size': page_size,
    #        'page_index': page_index,
    #        'total_items': 0,
    #        'items': []
    #        }
    #ret.sort(dict(
    #    effect_date = 1
    #    ))
    return ret