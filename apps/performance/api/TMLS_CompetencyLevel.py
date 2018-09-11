# -*- coding: utf-8 -*-
from bson import ObjectId
import models
from Query import KPIGroup
import logging
import threading
import common
logger = logging.getLogger(__name__)
global lock
lock = threading.Lock()

def get_list_with_searchtext(args):
    searchText = args['data'].get('search', '')
    pageSize = args['data'].get('pageSize', 0)
    pageIndex = args['data'].get('pageIndex', 20)
    sort = args['data'].get('sort', 20)

    pageIndex = (lambda pIndex: pIndex if pIndex != None else 0)(pageIndex)
    pageSize = (lambda pSize: pSize if pSize != None else 20)(pageSize)
    ret=models.TMLS_CompetencyLevel().aggregate()
    ret.left_join(models.auth_user_info(), "created_by", "username", "uc")
    ret.left_join(models.auth_user_info(), "modified_by", "username", "um")
    ret.project(
            com_code = "com_code",
            com_level_code = "com_level_code",
            com_level_name = "com_level_name",
            com_level_name2 = "com_level_name2",
            score_from = "score_from",
            score_to = "score_to",
            note = "note",
            ordinal = "ordinal",
            created_by="uc.login_account",
            created_on="created_on",
            modified_on="switch(case(modified_on!='',modified_on),'')",
            modified_by="switch(case(modified_by!='',um.login_account),'')",
        )
    ret.match("com_code == {0}", args['data']['com_code'])
    
    if(searchText != None):
        ret.match("contains(com_level_code, @name) or " + \
            "contains(com_level_name, @name) or " + \
            "contains(score_from, @name) or " + \
            "contains(score_to, @name)",name=searchText.strip())

    if(sort != None):
        ret.sort(sort)
        
    return ret.get_page(pageIndex, pageSize)

def get_competency_level(com_code, com_level_code):
    ret=models.TMLS_CompetencyLevel().aggregate()
    ret.left_join(models.auth_user_info(), "created_by", "username", "uc")
    ret.left_join(models.auth_user_info(), "modified_by", "username", "um")
    ret.project(
            com_code = "com_code",
            com_level_code = "com_level_code",
            com_level_name = "com_level_name",
            com_level_name2 = "com_level_name2",
            score_from = "score_from",
            score_to = "score_to",
            note = "note",
            ordinal = "ordinal",
            created_by="uc.login_account",
            created_on="created_on",
            modified_on="switch(case(modified_on!='',modified_on),'')",
            modified_by="switch(case(modified_by!='',um.login_account),'')",
        )
    ret.match("com_code == @com_code and com_level_code == @com_level_code", com_code = com_code, com_level_code = com_level_code)

    return ret.get_item()

def insert(args):
    try:
        lock.acquire()
        ret = {}
        if args['data'] != None:
            ret  =  models.TMLS_CompetencyLevel().insert(args['data'])
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
            data = args['data'].copy()
            del data['com_code']
            del data['com_level_code']
            ret  =  models.TMLS_CompetencyLevel().update(
                data, 
                "(com_code == @com_code) and (com_level_code == @com_level_code)",
                com_code = args['data']['com_code'],
                com_level_code = args['data']['com_level_code'])
            if ret['data'].raw_result['updatedExisting'] == True:
                ret.update(
                    item = get_competency_level(args['data']['com_code'], args['data']['com_level_code'])
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
            ret  =  models.TMLS_CompetencyLevel().delete(
                "com_code == {0} and com_level_code in {1}",
                args['data']['com_code'],
                args['data']['com_level_code'])
            lock.release()
            if ret['deleted'] > 0:
                models.TMLS_CompetencyAction().delete(
                "com_code == {0} and com_level_code in {1}", 
                args['data']['com_code'],
                args['data']['com_level_code'])
            return ret

        lock.release()
        return dict(
            error = "request parameter is not exist"
        )
    except Exception as ex:
        lock.release()
        raise(ex)