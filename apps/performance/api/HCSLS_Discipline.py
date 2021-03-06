# -*- coding: utf-8 -*-
from bson import ObjectId
import models
import common
from Query import Discipline
import logging
import threading
from hcs_authorization import action_type, authorization
logger = logging.getLogger(__name__)
global lock
import qmongo
lock = threading.Lock()

@authorization.authorise(action = action_type.Action.READ)
def get_list_with_searchtext(args):
    searchText = args['data'].get('search', '')
    pageSize = args['data'].get('pageSize', 0)
    pageIndex = args['data'].get('pageIndex', 20)
    sort = args['data'].get('sort', 20)

    pageIndex = (lambda pIndex: pIndex if pIndex != None else 0)(pageIndex)
    pageSize = (lambda pSize: pSize if pSize != None else 20)(pageSize)
    ret=Discipline.display_list_discipline()

    ret=common.filter_lock(ret, args)
    
    if(searchText != None):
        ret.match("contains(disc_name, @name) or " + \
            "contains(disc_code, @name) or " + \
            "contains(note, @name) or " + \
            "contains(ordinal, @name)",name=searchText.strip())

    if(sort != None):
        ret.sort(sort)
        
    return ret.get_page(pageIndex, pageSize)

@authorization.authorise(action = action_type.Action.CREATE)
def insert(args):
    try:
        lock.acquire()
        ret = {}
        if args['data'] != None:
            data =  set_dict_insert_data(args)
            ret  =  qmongo.models.HCSLS_Discipline.insert(data)
            lock.release()
            return ret

        lock.release()
        return dict(
            error = "request parameter is not exist"
        )
    except Exception as ex:
        lock.release()
        raise(ex)

@authorization.authorise(action = action_type.Action.WRITE)
def update(args):
    try:
        lock.acquire()
        ret = {}
        if args['data'] != None:
            data =  set_dict_update_data(args)
            ret  =  qmongo.models.HCSLS_Discipline.update(
                data, 
                "disc_code == {0}", 
                args['data']['disc_code'])
            if ret['data'].raw_result['updatedExisting'] == True:
                ret.update(
                    item = Discipline.display_list_discipline().match("disc_code == {0}", args['data']['disc_code']).get_item()
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

@authorization.authorise(action = action_type.Action.DELETE)
def delete(args):
    try:
        lock.acquire()
        ret = {}
        if args['data'] != None:
            ret  =  qmongo.models.HCSLS_Discipline.delete("disc_code in {0}",[x["disc_code"]for x in args['data']])
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
def set_dict_insert_data(args):
    ret_dict = dict()

    ret_dict.update(
        disc_code           = (lambda x : x['disc_code']         if x.has_key('disc_code')     else None )(args['data']),
        disc_name           = (lambda x : x['disc_name']         if x.has_key('disc_name')     else None )(args['data']),
        disc_name2          = (lambda x : x['disc_name2']        if x.has_key('disc_name2')    else None )(args['data']),
        is_due_salary       = (lambda x : x['is_due_salary']     if x.has_key('is_due_salary') else None )(args['data']),
        ordinal             = (lambda x : x['ordinal']           if x.has_key('ordinal')       else None )(args['data']),
        note                = (lambda x : x['note']              if x.has_key('note')          else None )(args['data']),
        lock                = (lambda x : x['lock']              if x.has_key('lock')          else None )(args['data'])
    )

    return ret_dict

@authorization.authorise(common = True)
def set_dict_update_data(args):
    ret_dict = set_dict_insert_data(args)
    del ret_dict['disc_code']
    return ret_dict