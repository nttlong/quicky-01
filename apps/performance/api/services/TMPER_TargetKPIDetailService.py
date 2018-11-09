# -*- coding: utf-8 -*-
from .. import models
import qmongo
from qmongo import transaction
import datetime
from bson import ObjectId
from .. import common

def get_list(args):

    searchText = args['data'].get('search', '')
    pageSize = args['data'].get('pageSize', 0)
    pageIndex = args['data'].get('pageIndex', 20)
    sort = args['data'].get('sort', 20)

    pageIndex = (lambda pIndex: pIndex if pIndex != None else 0)(pageIndex)
    pageSize = (lambda pSize: pSize if pSize != None else 20)(pageSize)
    search = (lambda x: x.strip() if searchText != None else "")(searchText)

    collection = qmongo.models.TMPER_TargetKPIDetail.aggregate
    collection.left_join(models.auth_user_info(), "created_by", "username", "uc")
    collection.left_join(models.auth_user_info(), "modified_by", "username", "um")
    collection.project(
        rec_id=1,
        ref_id=1,
        apr_period=1,
        apr_year=1,
        employee_code=1,
        target_name=1,
        perform_date=1,
        perform=1,
        note=1,
        created_by="uc.login_account",
        created_on="created_on",
        modified_on="switch(case(modified_on!='',modified_on),'')",
        modified_by="switch(case(modified_by!='',um.login_account),'')"
    )
    collection.match("ref_id == @ref_id", ref_id = args['data']['rec_id'])

    if (searchText != None):
        collection.match("contains(target_name, @name) or contains(unit_name, @name)" + \
                  " or contains(weight, @name) or contains(target, @name)" +\
                  " or contains(min_value, @name) or contains(max_value, @name)" + \
                  " or contains(origin_target, @name)", name=search.strip())

    if (sort != None):
        collection.sort(sort)

    return collection.get_page(pageIndex, pageSize)

