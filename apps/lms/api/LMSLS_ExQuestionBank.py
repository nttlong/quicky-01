# -*- coding: utf-8 -*-
from bson import ObjectId
import models
import logging
import threading
import common
import random
logger = logging.getLogger(__name__)
global lock
lock = threading.Lock()
import qmongo
def get_list_data():
    items = qmongo.models.LMSLS_ExQuestionBank.aggregate
    items.left_join(qmongo.models.auth_user_info, "created_by", "username", "uc")
    items.left_join(qmongo.models.auth_user_info, "modified_by", "username", "um")
    items.project(
        ques_id=1,
        ques_category=1,
        ques_type=1,
        ques_level=1,
        ques_file=1,
        ques_detail_1=1,
        ques_detail_2=1,
        ques_hint=1,
        ques_answers=1,
        ques_total_marks=1,
        ques_attach_file=1,
        ques_max_answer_time=1,
        ques_explanation=1,
        ques_answer_options=1,
        ques_randomization=1,
        ques_tags=1,
        ques_evaluated_by=1,
        ques_limit_on_text=1,
        ques_specify_limit=1,
        created_by="uc.login_account",
        created_on="created_on",
        modified_on="switch(case(modified_on!='',modified_on),'')",
        modified_by="switch(case(modified_by!='',um.login_account),'')",
        )
    
    return items
def get_list_with_searchtext(args):
    searchText = args['data'].get('search', '')
    pageSize = args['data'].get('pageSize', 0)
    pageIndex = args['data'].get('pageIndex', 20)
    sort = args['data'].get('sort', 20)
    where = args['data'].get('where')

    pageIndex = (lambda pIndex: pIndex if pIndex != None else 0)(pageIndex)
    pageSize = (lambda pSize: pSize if pSize != None else 20)(pageSize)
    ret=qmongo.models.LMSLS_ExQuestionBank.aggregate
    ret.project(
            ques_id=1,
            ques_category=1,
            ques_type=1,
            ques_level=1,
            ques_file=1,
            ques_detail_1=1,
            ques_detail_2=1,
            ques_hint=1,
            ques_answers=1,
            ques_total_marks=1,
            ques_attach_file=1,
            ques_max_answer_time=1,
            ques_explanation=1,
            ques_answer_options=1,
            ques_randomization=1,
            ques_tags=1,
            ques_evaluated_by=1,
            ques_limit_on_text=1,
            ques_specify_limit=1,
            created_on="created_on",
        )
    
    if(where != None):
        ret.match("(ques_category==@ques_category)",ques_category=where['ques_category'])

    if(searchText != None and searchText !='' ):
        ret.match("contains(ques_detail_1, @name) or contains(ques_detail_2, @name)",name=searchText)

    if(sort != None):
        ret.sort(sort)
        
    data = ret.get_page(pageIndex, pageSize)
    return  data
def get_list_with_list_ques_id(args):
    searchText = args['data'].get('search', '')
    pageSize = args['data'].get('pageSize', 0)
    pageIndex = args['data'].get('pageIndex', 20)
    sort = args['data'].get('sort', 20)
    where = args['data'].get('where')
    pageIndex = (lambda pIndex: pIndex if pIndex != None else 0)(pageIndex)
    pageSize = (lambda pSize: pSize if pSize != None else 20)(pageSize)
    ret=qmongo.models.LMSLS_ExQuestionBank.aggregate

    ret.project(
            ques_id=1,
            ques_category=1,
            ques_type=1,
            ques_level=1,
            ques_file=1,
            ques_detail_1=1,
            ques_detail_2=1,
            ques_hint=1,
            ques_answers=1,
            ques_total_marks=1,
            ques_attach_file=1,
            ques_max_answer_time=1,
            ques_explanation=1,
            ques_answer_options=1,
            ques_randomization=1,
            ques_tags=1,
            ques_evaluated_by=1,
            ques_limit_on_text=1,
            ques_specify_limit=1,

        )
    
    if(where != None):
        ret.match("ques_id in {0}", where['list_ques'])


    if(sort != None):
        ret.sort(sort)
        
    data = ret.get_page(pageIndex, pageSize)
    return  data
def get_list_with_random_ques_id(args):
    where = args['data'].get('where')
    ret= qmongo.models.LMSLS_ExQuestionBank.aggregate
    if(where != None):
        ret.match("(ques_category==@ques_category)",ques_category=where['assign']['category'])
    ret.project(
            ques_id=1,
            ques_category=1,
            ques_level=1,
        )
    conques = ret.get_list()
    diff_ques= filter(lambda x: x['ques_level'] == 1, conques)
    med_ques= filter(lambda x: x['ques_level'] == 2, conques)
    easy_ques= filter(lambda x: x['ques_level'] == 3, conques)
    if(where['assign']['diff_ques']!= None):
        if(where['assign']['diff_ques'] < len(diff_ques)):
            diff_ques=random.sample(diff_ques,where['assign']['diff_ques'])
    else:
        diff_ques=[]
    if(where['assign']['med_ques']!= None):
        if(where['assign']['med_ques'] < len(med_ques)):
            med_ques=random.sample(med_ques,where['assign']['med_ques'])
    else:
        med_ques=[]
    if(where['assign']['easy_ques']!= None):
        if(where['assign']['easy_ques'] < len(easy_ques)):
            easy_ques=random.sample(easy_ques,where['assign']['easy_ques'])
    else:
        easy_ques=[]
    return dict(
           list_ques = diff_ques + med_ques + easy_ques
        )

def insert(args):
    try:
        lock.acquire()
        ret = {}
        if args['data'] != None:
            data =  set_dict_insert_data(args)
            ret  = qmongo.models.LMSLS_ExQuestionBank.insert(data)
            lock.release()
            return ret

        lock.release()
        return dict(
            error = "request parameter is not exist"
        )
    except Exception as ex:
        lock.release()
        raise(ex)

def insertanswer(args):
    try:
        lock.acquire()
        ret = {}
        if args['data'] != None:
            data =  set_dict_insert_data(args)
            ret  = qmongo.models.LMSLS_ExQuestionBank.aggregate
            lock.release()
            return ret

        lock.release()
        return dict(
            error = "request parameter is not exist"
        )
    except Exception as ex:
        lock.release()
        raise(ex)

def updateanswer(args):
    try:
        lock.acquire()
        ret = {}
        if args['data'] != None:
            data =  set_dict_update_data(args)
            ret  =  qmongo.models.LMSLS_MaterialFolder.update(
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

def update(args):
    try:
        lock.acquire()
        ret = {}
        if args['data'] != None:
            data =  set_dict_update_data(args)
            ret  =  qmongo.models.LMSLS_MaterialFolder.update(
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
            ret  = qmongo.models.LMSLS_ExQuestionBank.delete("_id in {0}",[ObjectId(x["_id"])for x in args['data']])
            lock.release()
            return ret

        lock.release()
        return dict(
            error = "request parameter is not exist"
        )
    except Exception as ex:
        lock.release()
        raise(ex)

def set_dict_answer_insert_data():
    ret_dict = dict()
    ret_dict.update(


    )

def set_dict_insert_data(args):
    ret_dict = dict()

    ret_dict.update(
        ques_id= (lambda x: x['ques_id'] if x.has_key('ques_id') else None)(args['data']),
        ques_category= (lambda x: x['ques_category'] if x.has_key('ques_category') else None)(args['data']),
        ques_type= (lambda x: x['ques_type'] if x.has_key('ques_type') else None)(args['data']),
        ques_level= (lambda x: x['ques_level'] if x.has_key('ques_level') else None)(args['data']),
        ques_file= (lambda x: x['ques_file'] if x.has_key('ques_file') else None)(args['data']),
        ques_detail_1= (lambda x: x['ques_detail_1'] if x.has_key('ques_detail_1') else None)(args['data']),
        ques_detail_2= (lambda x: x['ques_detail_2'] if x.has_key('ques_detail_2') else None)(args['data']),
        ques_hint= (lambda x: x['ques_hint'] if x.has_key('ques_hint') else None)(args['data']),
        ques_answers= (lambda x: x['ques_answers'] if x.has_key('ques_answers') else None)(args['data']),
        ques_total_marks= (lambda x: x['ques_total_marks'] if x.has_key('ques_total_marks') else None)(args['data']),
        ques_attach_file= (lambda x: x['ques_attach_file'] if x.has_key('ques_attach_file') else None)(args['data']),
        ques_max_answer_time= (lambda x: x['ques_max_answer_time'] if x.has_key('ques_max_answer_time') else 0)(args['data']),
        ques_explanation= (lambda x: x['ques_explanation'] if x.has_key('ques_explanation') else None)(args['data']),
        ques_answer_options= (lambda x: x['ques_answer_options'] if x.has_key('ques_answer_options') else None)(args['data']),
        ques_randomization= (lambda x: x['ques_randomization'] if x.has_key('ques_randomization') else None)(args['data']),
        ques_tags= (lambda x: x['ques_tags'] if x.has_key('ques_tags') else None)(args['data']),
        ques_limit_on_text= (lambda x: x['ques_limit_on_text'] if x.has_key('ques_limit_on_text') else None)(args['data']),
        ques_specify_limit= (lambda x: x['ques_specify_limit'] if x.has_key('ques_specify_limit') else None)(args['data']),
        ques_evaluated_by= (lambda x: x['ques_evaluated_by'] if x.has_key('ques_evaluated_by') else None)(args['data']),
    )

    return ret_dict

def set_dict_update_data(args):
    ret_dict = set_dict_insert_data(args)
    return ret_dict
def get_level_code_by_folder_id(args):
    where = args['data'].get('where')
    ret=qmongo.models.LMSLS_MaterialFolder.aggregate
    if(where != None):
        ret.match("(folder_id==@folder_id)",folder_id=where['folder_id'])
    ret.project(
        level_code=1
        )
    return ret.get_page(0, 100)