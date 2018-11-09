# -*- coding: utf-8 -*-
from bson import ObjectId
import  qmongo
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
    ret = qmongo.models.TMLS_CompetencyFactor.aggregate
    ret.left_join(qmongo.models.auth_user_info, "created_by", "username", "uc")
    ret.left_join(qmongo.models.auth_user_info, "modified_by", "username", "um")
    ret.project(
        com_code="com_code",
        factor="factor",
        weight="weight",
        com_level_code="com_level_code",
        ordinal="ordinal",
        created_by="uc.login_account",
        created_on="created_on",
        modified_on="switch(case(modified_on!='',modified_on),'')",
        modified_by="switch(case(modified_by!='',um.login_account),'')",
    )
    ret.match('com_code == {0}', args['data']['com_code'])

    if (searchText != None):
        ret.match("contains(factor, @name) or " + \
                  "contains(weight, @name) or contains(com_level_code, @name)", name=searchText.strip())

    if (sort != None):
        ret.sort(sort)

    return ret.get_page(pageIndex, pageSize)


def get_competency_factor(com_code, factor):
    ret = qmongo.models.TMLS_CompetencyFactor.aggregate
    ret.left_join(qmongo.models.auth_user_info, "created_by", "username", "uc")
    ret.left_join(qmongo.models.auth_user_info, "modified_by", "username", "um")
    ret.project(
        com_code="com_code",
        factor="factor",
        weight="weight",
        com_level_code="com_level_code",
        ordinal="ordinal",
        created_by="uc.login_account",
        created_on="created_on",
        modified_on="switch(case(modified_on!='',modified_on),'')",
        modified_by="switch(case(modified_by!='',um.login_account),'')",
    )
    ret.match("com_code == @com_code and factor == @factor",
              com_code=com_code,
              factor=factor)
    return ret.get_item()


def insert(args):
    try:
        lock.acquire()
        ret = {}
        if args['data'] != None:
            del args['data']['_id']
            ret = qmongo.models.TMLS_CompetencyFactor.insert(args['data'])
            lock.release()
            return ret

        lock.release()
        return dict(
            error="request parameter is not exist"
        )
    except Exception as ex:
        lock.release()
        raise (ex)


def update(args):
    try:
        lock.acquire()
        ret = {}
        if args['data'] != None:
            data = args['data'].copy()
            del data['com_code']
            del data['_id']
            ret = qmongo.models.TMLS_CompetencyFactor.update(
                data,
                "com_code == @com_code and _id == @_id",
                com_code=args['data']['com_code'],
                _id=ObjectId(args['data']['_id']))
            if ret['data'].raw_result['updatedExisting'] == True:
                ret.update(
                    item=get_competency_factor(args['data']['com_code'],
                                               args['data']['factor'])
                )
            lock.release()
            return ret

        lock.release()
        return dict(
            error="request parameter is not exist"
        )
    except Exception as ex:
        lock.release()
        raise (ex)


def delete(args):
    try:
        lock.acquire()
        ret = {}
        if args['data'] != None:
            ret = qmongo.models.TMLS_CompetencyFactor.delete(
                "com_code == {0} and _id in {1}",
                args['data']['com_code'],
                [ObjectId(x) for x in args['data']['_id']])
            lock.release()
            return ret

        lock.release()
        return dict(
            error="request parameter is not exist"
        )
    except Exception as ex:
        lock.release()
        raise (ex)