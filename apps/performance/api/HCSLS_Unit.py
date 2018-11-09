# -*- coding: utf-8 -*-
from bson import ObjectId
import qmongo
import models
import common
from Query import Unit
import logging
import threading
from hcs_authorization import action_type, authorization
logger = logging.getLogger(__name__)
global lock
lock = threading.Lock()

@authorization.authorise(action = action_type.Action.READ)
def get_list_with_searchtext(args):
    searchText = args['data'].get('search', '')
    pageSize = args['data'].get('pageSize', 0)
    pageIndex = args['data'].get('pageIndex', 20)
    sort = args['data'].get('sort', 20)

    pageIndex = (lambda pIndex: pIndex if pIndex != None else 0)(pageIndex)
    pageSize = (lambda pSize: pSize if pSize != None else 20)(pageSize)
    ret=Unit.display_list_unit()

    ret=common.filter_lock(ret, args)
    
    if(searchText != None):
        ret.match("contains(unit_code, @name) or " + \
            "contains(unit_name, @name) or " + \
            "contains(unit_name2, @name) or " + \
            "contains(note, @name) or " + \
            "contains(lock, @name) or " + \
            "contains(ordinal, @name)",name=searchText.strip())

    if(sort != None):
        ret.sort(sort)
        
    return ret.get_page(pageIndex, pageSize)

@authorization.authorise(action = action_type.Action.READ)
def get_default_vale(args):
    return qmongo.models.HCSLS_Unit.aggregate.match("is_default == {0}", True).get_item()

@authorization.authorise(action = action_type.Action.CREATE)
def insert(args):
    try:
        lock.acquire()
        ret = {}
        if args['data'] != None:
            data =  set_dict_insert_data(args)

            # if len(models.HCSLS_Unit().get_list()) == 0:
            #     set_dict_is_default_true(data)

            ret  =  qmongo.models.HCSLS_Unit.insert(data)

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

            if args['data']['is_default'] != None and args['data']['is_default'] == True:
                update_is_default(args)

            ret  =  qmongo.models.HCSLS_Unit.update(
                data, 
                "_id == {0}",
                ObjectId(args['data']["_id"]))
            if ret['data'].raw_result['updatedExisting'] == True:
                ret.update(
                    item = Unit.display_list_unit().match("unit_code == {0}", args['data']['unit_code']).get_item()
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
            ret  = qmongo.models.HCSLS_Unit.delete("unit_code in {0}",[x["unit_code"]for x in args['data']])
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
def delete_one(id):
    try:
        lock.acquire()
        ret = {}
        if id['data'] != '':
            ret  = qmongo.models.HCSLS_Unit.delete("_id == {0}", ObjectId(id['data']))
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
        unit_code      = (lambda x: x['unit_code']      if x.has_key('unit_code')       else None)(args['data']),
        unit_name      = (lambda x: x['unit_name']      if x.has_key('unit_name')       else None)(args['data']),
        unit_name2     = (lambda x: x['unit_name2']     if x.has_key('unit_name2')      else None)(args['data']),
        ordinal            = (lambda x: x['ordinal']            if x.has_key('ordinal')             else None)(args['data']),
        note               = (lambda x: x['note']               if x.has_key('note')                else None)(args['data']),
        lock               = (lambda x: x['lock']               if x.has_key('lock')                else None)(args['data']),
        is_default         = (lambda x: x['is_default']         if x.has_key('is_default')          else None)(args['data']),
        data_type          = (lambda x: x['data_type']          if x.has_key('data_type')           else None)(args['data']),
        dec_place          = (lambda x: x['dec_place']          if x.has_key('dec_place')           else None)(args['data']),
        value_list_detail  = (lambda x: x['value_list_detail']  if x.has_key('value_list_detail')   else None)(args['data']),
    )

    return ret_dict

@authorization.authorise(common = True)
def set_dict_update_data(args):
    ret_dict = set_dict_insert_data(args)
    del ret_dict['unit_code']
    return ret_dict

@authorization.authorise(common = True)
def update_is_default(args):
    try:

        ret = common.get_collection('HCSLS_Unit').update_many(
            {"is_default": True},
            {"$set": {"is_default": False}}
        )

        ret = models.HCSLS_Unit().update(
            {"is_default": True},
            "_id == {0}",
            ObjectId(args['data']["_id"]))

    except Exception as ex:
        raise(ex)

def set_dict_is_default_true(data):

    data.update(
        is_default=True,
    )

    return data