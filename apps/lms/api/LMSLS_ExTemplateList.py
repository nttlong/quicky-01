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
#    items = models.LMSLS_ExTemplateList().aggregate()
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
    ret=models.LMSLS_ExTemplateList().aggregate()
    ret.project(
            exam_temp_id=1,
            exam_temp_category=1,
            exam_temp_name1=1,
            exam_temp_name2=1,
            duration=1,
            negative_marks=1,
            mode_pick=1,
            creator=1,
            question_list=1,
            total_question=1,
            total_mask=1,
            easy_question=1,
            med_question=1,
            diff_question=1,
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
            for i in args['data']['question_list']:                 
                if i.has_key('$$regKey'):
                    del i['$$regKey']
                if i.has_key('$$selectKey'):
                    del i['$$selectKey']
                if i.has_key('$$hashKey'):
                    del i['$$hashKey']
                if i.has_key('list_permision'):
                    for a in i['list_permision']:
                        if a.has_key('$$regKey'):
                            del a['$$regKey']
                        if a.has_key('$$selectKey'):
                            del a['$$selectKey']
                        if a.has_key('$$hashKey'):
                            del a['$$hashKey']
            data =  set_dict_insert_data(args)
            ret  =  models.LMSLS_ExTemplateList().insert(data)
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
            ret  =  models.LMSLS_ExTemplateList().update(
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
            ret  =  models.LMSLS_ExTemplateList().delete("_id in {0}",[ObjectId(x["_id"])for x in args['data']])
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
        exam_temp_id= (lambda x: x['exam_temp_id'] if x.has_key('exam_temp_id') else None)(args['data']),
        exam_temp_category= (lambda x: x['exam_temp_category'] if x.has_key('exam_temp_category') else None)(args['data']),
        exam_temp_name1= (lambda x: x['exam_temp_name1'] if x.has_key('exam_temp_name1') else None)(args['data']),
        exam_temp_name2= (lambda x: x['exam_temp_name2'] if x.has_key('exam_temp_name2') else None)(args['data']),
        duration= (lambda x: x['duration'] if x.has_key('duration') else None)(args['data']),
        creator= (lambda x: x['creator'] if x.has_key('creator') else None)(args['data']),
        negative_marks= (lambda x: x['negative_marks'] if x.has_key('negative_marks') else None)(args['data']),
        mode_pick= (lambda x: x['mode_pick'] if x.has_key('mode_pick') else None)(args['data']),
        question_list= (lambda x: x['question_list'] if x.has_key('question_list') else None)(args['data']),
        total_question= (lambda x: x['total_question'] if x.has_key('total_question') else None)(args['data']),
        total_mask= (lambda x: x['total_mask'] if x.has_key('total_mask') else None)(args['data']),
        easy_question= (lambda x: x['easy_question'] if x.has_key('easy_question') else None)(args['data']),
        med_question= (lambda x: x['med_question'] if x.has_key('med_question') else None)(args['data']),
        diff_question= (lambda x: x['diff_question'] if x.has_key('diff_question') else None)(args['data']),
    )

    return ret_dict

def set_dict_update_data(args):
    ret_dict = set_dict_insert_data(args)
    del ret_dict['category_id']
    return ret_dict
#def get_level_code_by_folder_id(args):
#    where = args['data'].get('where')
#    ret=models.LMSLS_ExTemplateList().aggregate()
#    if(where != None):
#        ret.match("(folder_id==@folder_id)",folder_id=where['folder_id'])
#    ret.project(
#        level_code=1
#        )
#    return ret.get_page(0, 100)