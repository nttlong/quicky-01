# -*- coding: utf-8 -*-
from bson import ObjectId
import qmongo
import models
import common
from Query import Region
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
    ret=Region.display_list_region()

    ret=common.filter_lock(ret, args)
    
    if(searchText != None):
        ret.match("contains(region_name, @name) or " + \
            "contains(region_code, @name) or " + \
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
            ret  =  qmongo.models.HCSLS_Region.insert(data)
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
            ret  = qmongo.models.HCSLS_Region.update(
                data, 
                "region_code == {0}", 
                args['data']['region_code'])
            if ret['data'].raw_result['updatedExisting'] == True:
                ret.update(
                    item = Region.display_list_region().match("region_code == {0}", args['data']['region_code']).get_item()
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
            ret  =  qmongo.models.HCSLS_Region.delete("region_code in {0}",[x["region_code"]for x in args['data']])
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
        region_code        = (lambda x : x['region_code']      if x.has_key('region_code')  else None )(args['data']),
        region_name        = (lambda x : x['region_name']      if x.has_key('region_name')  else None )(args['data']),
        region_name2       = (lambda x : x['region_name2']     if x.has_key('region_name2') else None )(args['data']),
        ordinal            = (lambda x : x['ordinal']          if x.has_key('ordinal')      else None )(args['data']),
        note               = (lambda x : x['note']             if x.has_key('note')         else None )(args['data']),
        lock               = (lambda x : x['lock']             if x.has_key('lock')         else None )(args['data'])
    )

    return ret_dict

@authorization.authorise(common = True)
def set_dict_update_data(args):
    ret_dict = set_dict_insert_data(args)
    del ret_dict['region_code']
    return ret_dict