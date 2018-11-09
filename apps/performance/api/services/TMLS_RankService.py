from .. import common
import datetime
from .. import models
from .. import TMSYS_ConfigChangeObjectPriority
def set_dict_detail_update_data(args, rank_code):
    ret_dict = set_dict_detail_insert_data(args, rank_code)
    del ret_dict['rec_id']
    ret_dict['modified_on'] = datetime.datetime.now()
    ret_dict['modified_by'] = common.get_user_id()
    return ret_dict

def set_dict_detail_insert_data(args, rank_code):
    ret_dict = dict()
    change_object = []
    object = {}
    object_name = ""
    column_name = ""
    if args.has_key('change_object') and args.has_key('object_code'):
        change_object = TMSYS_ConfigChangeObjectPriority.get_list({"data":{"name":"TMChangeObjectRank"}})
        for x in change_object:
            if x['change_object'] == args['change_object']:
                object = x
                break
        __collection = getattr(models, object['table_name'])()
        if object['change_object'] == 1:
            column_name = "gjw_code"
            ret = __collection.aggregate().project(gjw_code = 1, gjw_name = 1)
            object_name = ret.match(column_name + " in {0}", args['object_code']).get_item()['gjw_name']
        elif object['change_object'] == 2:
            column_name = "job_w_code"
            ret = __collection.aggregate().project(job_w_code = 1, job_w_name = 1)
            object_name = ret.match(column_name + " in {0}", args['object_code']).get_item()['job_w_name']
        elif object['change_object'] == 3:
            column_name = "job_pos_code"
            ret = __collection.aggregate().project(job_pos_code = 1, job_pos_name = 1)
            object_name = ret.match(column_name + " == {0}", args['object_code']).get_item()['job_pos_name']
        elif object['change_object'] == 4:
            column_name = "emp_type_code"
            ret = __collection.aggregate().project(emp_type_code = 1, emp_type_name = 1)
            object_name = ret.match(column_name + " == {0}", args['object_code']).get_item()['emp_type_name']
    else:
        return None

    ret_dict.update(
            rec_id            = common.generate_guid(),
            rank_code         = rank_code,
            change_object     = (lambda x: x['change_object']  if x.has_key('change_object')    else None)(args),
            object_level      = None,
            object_code       = (lambda x: x['object_code']    if x.has_key('object_code')      else None)(args),
            object_name       = object_name,
            priority_no       = object['priority_no'],
            total_from        = (lambda x: x['total_from']     if x.has_key('total_from')       else None)(args),
            total_to          = (lambda x: x['total_to']       if x.has_key('total_to')         else None)(args),
            note              = (lambda x: x['note']           if x.has_key('note')             else None)(args),
            created_on        = datetime.datetime.now(),
            created_by        = common.get_user_id(),
            modified_on       = "",
            modified_by       = ""
            )
    return ret_dict