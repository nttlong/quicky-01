# -*- coding: utf-8 -*-
from bson import ObjectId
import models
import logging
import threading
import common
logger = logging.getLogger(__name__)
global lock
lock = threading.Lock()

#def get_list_data():
#    items = models.LMSLS_ExResultType().aggregate()
#    items.left_join(models.auth_user_info(), "created_by", "username", "uc")
#    items.left_join(models.auth_user_info(), "modified_by", "username", "um")
#    items.project(
#        folder_id=1,
#        folder_name=1,
#        folder_name2=1,
#        parent_id=1,
#        parent_code=1,
#        level=1,
#        level_code=1,
#        ordinal=1,
#        lock=1,
#        note=1,
#        moderator_id=1,
#        approver_id=1,
#        active=1,
#        permisions=1,
#        approve_type=1,
#        created_by="uc.login_account",
#        created_on="created_on",
#        modified_on="switch(case(modified_on!='',modified_on),'')",
#        modified_by="switch(case(modified_by!='',um.login_account),'')",
#        )
    
#    return items
def get_list_with_searchtext(args):
    searchText = args['data'].get('search', '')
    pageSize = args['data'].get('pageSize', 0)
    pageIndex = args['data'].get('pageIndex', 20)
    sort = args['data'].get('sort', 20)
    where = args['data'].get('where')

    pageIndex = (lambda pIndex: pIndex if pIndex != None else 0)(pageIndex)
    pageSize = (lambda pSize: pSize if pSize != None else 20)(pageSize)
    ret=models.LMSLS_ExResultType().aggregate()
    ret.project(
            result_type_id=1,
            result_type1=1,
            creator=1,
            created_on=1,
        )
  
    if(sort != None):
        ret.sort(sort)
        
    data = ret.get_page(pageIndex, pageSize)
    return  data

def insert(args):
    try:
        lock.acquire()
        ret = {}
        if args['data'] != None:
            data =  set_dict_insert_data(args)
            ret  =  models.LMSLS_ExResultType().insert(data)
            lock.release()
            return ret

        lock.release()
        return dict(
            error = "request parameter is not exist"
        )
    except Exception as ex:
        lock.release()
        raise(ex)

def update(args):
    try:
        lock.acquire()
        ret = {}
        if args['data'] != None:
            data =  set_dict_update_data(args)
            ret  =  models.LMSLS_ExResultType().update(
                data, 
                "_id == {0}", 
                ObjectId(args['data']['_id']))
            if ret['data'].raw_result['updatedExisting'] == True:
                ret.update(
                    item = get_list_data().match("_id == {0}", ObjectId(args['data']['_id'])).get_item()
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

def delete(args):
    try:
        lock.acquire()
        ret = {}
        if args['data'] != None:
            ret  =  models.LMSLS_ExResultType().delete("_id in {0}",[ObjectId(x["_id"])for x in args['data']])
            lock.release()
            return ret

        lock.release()
        return dict(
            error = "request parameter is not exist"
        )
    except Exception as ex:
        lock.release()
        raise(ex)

def set_dict_insert_data(args):
    ret_dict = dict()

    ret_dict.update(
        result_type_id= (lambda x: x['result_type_id'] if x.has_key('result_type_id') else None)(args['data']),
        result_type1= (lambda x: x['result_type1'] if x.has_key('result_type1') else None)(args['data']),
        result_type2= (lambda x: x['result_type2'] if x.has_key('result_type2') else None)(args['data']),
        grading_scale= (lambda x: x['grading_scale'] if x.has_key('grading_scale') else None)(args['data']),
        order= (lambda x: x['order'] if x.has_key('order') else None)(args['data']),
        note= (lambda x: x['note'] if x.has_key('note') else None)(args['data']),
        active= (lambda x: x['active'] if x.has_key('active') else None)(args['data']),
        creator= (lambda x: x['creator'] if x.has_key('creator') else None)(args['data']),
        created_on= (lambda x: x['created_on'] if x.has_key('created_on') else None)(args['data']),
        created_by= (lambda x: x['created_by'] if x.has_key('created_by') else None)(args['data']),
        modified_on= (lambda x: x['total_question'] if x.has_key('total_question') else None)(args['data']),
        modified_by= (lambda x: x['total_mask'] if x.has_key('total_mask') else None)(args['data']),
        
    )

    return ret_dict

def set_dict_update_data(args):
    ret_dict = set_dict_insert_data(args)
    del ret_dict['category_id']
    return ret_dict
def get_list(args):
        try:
            items = common.get_collection('LMSLS_ExResultType').aggregate([
                    {
                        "$limit": 10000
                    },
                    {
                    "$group":
                        {
                        "_id": 1,
                        "value_list": {"$push": {"result_type1": '$result_type1'}}
                        }
                    },
                    {
                        "$unwind": {"path": '$value_list', "includeArrayIndex": 'value'
                         }
                    },
                    {
                        "$project": {
                        "caption": '$value_list.result_type1',
                        "value": 1
                        }
                    }
                    ])
            return (list(items))         
        except Exception as ex:
            raise(ex)
