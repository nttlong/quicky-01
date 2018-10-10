# -*- coding: utf-8 -*-
from bson import ObjectId
import models
import logging
import threading
import common
import random
import datetime
import qmongo

logger = logging.getLogger(__name__)
global lock
lock = threading.Lock()

def get_list_data():
    items = models.LMSLS_Topic().aggregate()
    items.left_join(models.auth_user_info(), "created_by", "username", "uc")
    items.left_join(models.auth_user_info(), "modified_by", "username", "um")
    items.project(
        topic_id=1,
        topic_name=1,
        topic_name_other=1,
        forum_id=1,
        topic_description=1,

        publish=1,
        publish_date=1,
        allow_replies=1,

        topic_replies=1,
        topic_views=1,
        approved_by=1,
        approved_on=1,
        rejected_by=1,
        rejected_on=1,
        feedback=1,
        topic_approved=1,
        topic_removed=1,
        topic_pin=1,
        topic_block=1,

        created_by="uc.login_account",
        created_on="created_on",
        modified_on="switch(case(modified_on!='',modified_on),'')",
        modified_by="switch(case(modified_by!='',um.login_account),'')",
    )
    return items

def get_list_with_searchtext_draft(args):
    searchText = args['data'].get('search', '')
    pageSize = args['data'].get('pageSize', 0)
    pageIndex = args['data'].get('pageIndex', 20)
    sort = args['data'].get('sort', 20)
    where = args['data'].get('where')

    pageIndex = (lambda pIndex: pIndex if pIndex != None else 0)(pageIndex)
    pageSize = (lambda pSize: pSize if pSize != None else 20)(pageSize)
    ret = models.LMSLS_Topic().aggregate()
    ret.match("(publish=={0} and topic_removed=={1})", False, False)
    ret.left_join(models.auth_user_info(), "created_by", "username", "uc")
    ret.left_join(models.auth_user_info(), "modified_by", "username", "um")
    ret.left_join(models.LMSLS_Forum(), "forum_id", "forum_id", "fr")

    if (where != None):
        if (where.has_key('parent_code') and (where['parent_code'] == None or where['parent_code'] == '0')): # là node cha
            if (where.has_key('forum_id') and where['forum_id'] != None): # kiểm tra id của node cha
                if(where['forum_id'] == 0 or where['forum_id'] == '0'): #lấy all topic
                    pass
                elif (where['forum_id'] == 1 or where['forum_id'] == '1'): # lấy topic của forum public
                    ret.match("(fr.forum_type=={0})", True)
                elif (where['forum_id'] == 2 or where['forum_id'] == '2'): # lấy topic của forum private
                    ret.match("(fr.forum_type=={0})", False)
        else:
            if (where.has_key('forum_id') and where['forum_id'] != None):
                ret.match("(forum_id=={0})", where['forum_id'])

    ret.project(
        topic_id=1,
        topic_name=1,
        topic_name_other=1,
        forum_id=1,
        topic_description=1,

        publish=1,
        publish_date=1,
        allow_replies=1,

        topic_replies=1,
        topic_views=1,
        topic_approved=1,
        topic_removed=1,

        created_by="uc.login_account",
        created_on="created_on",
        modified_on="switch(case(modified_on!='',modified_on),'')",
        modified_by="switch(case(modified_by!='',um.login_account),'')",
    )

    if (searchText != None and searchText != ''):
        ret.match("contains(topic_name, @name) or contains(topic_description, @name)", name=searchText)

    if (sort != None):
        ret.sort(sort)

    data = ret.get_page(pageIndex, pageSize)
    return data

def get_list_with_searchtext_pending(args):
    searchText = args['data'].get('search', '')
    pageSize = args['data'].get('pageSize', 0)
    pageIndex = args['data'].get('pageIndex', 20)
    sort = args['data'].get('sort', 20)
    where = args['data'].get('where')

    pageIndex = (lambda pIndex: pIndex if pIndex != None else 0)(pageIndex)
    pageSize = (lambda pSize: pSize if pSize != None else 20)(pageSize)
    ret = models.LMSLS_Topic().aggregate()
    ret.match("publish == {0} and topic_approved == {1} and topic_removed=={2}", True, None, False)
    ret.left_join(models.auth_user_info(), "created_by", "username", "uc")
    ret.left_join(models.auth_user_info(), "modified_by", "username", "um")
    ret.left_join(models.LMSLS_Forum(), "forum_id", "forum_id", "fr")

    if (where != None):
        if (where.has_key('parent_code') and (where['parent_code'] == None or where['parent_code'] == '0')): # là node cha
            if (where.has_key('forum_id') and where['forum_id'] != None): # kiểm tra id của node cha
                if(where['forum_id'] == 0 or where['forum_id'] == '0'): #lấy all topic
                    pass
                elif (where['forum_id'] == 1 or where['forum_id'] == '1'): # lấy topic của forum public
                    ret.match("(fr.forum_type=={0})", True)
                elif (where['forum_id'] == 2 or where['forum_id'] == '2'): # lấy topic của forum private
                    ret.match("(fr.forum_type=={0})", False)
        else:
            if (where.has_key('forum_id') and where['forum_id'] != None):
                ret.match("(forum_id=={0})", where['forum_id'])

    ret.project(
        topic_id=1,
        topic_name=1,
        topic_name_other=1,
        forum_id=1,
        topic_description=1,

        publish=1,
        publish_date=1,
        allow_replies=1,

        topic_replies=1,
        topic_views=1,
        topic_approved=1,
        topic_removed=1,

        created_by="uc.login_account",
        created_on="created_on",
        modified_on="switch(case(modified_on!='',modified_on),'')",
        modified_by="switch(case(modified_by!='',um.login_account),'')",
    )

    if (searchText != None and searchText != ''):
        ret.match("contains(topic_name, @name) or contains(topic_description, @name)", name=searchText)

    if (sort != None):
        ret.sort(sort)

    data = ret.get_page(pageIndex, pageSize)
    return data

def get_list_with_searchtext_published(args):
    searchText = args['data'].get('search', '')
    pageSize = args['data'].get('pageSize', 0)
    pageIndex = args['data'].get('pageIndex', 20)
    sort = args['data'].get('sort', 20)
    where = args['data'].get('where')

    fisttimedate = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    lasttimedate = datetime.datetime.now().replace(hour=23, minute=59, second=59, microsecond=0)

    pageIndex = (lambda pIndex: pIndex if pIndex != None else 0)(pageIndex)
    pageSize = (lambda pSize: pSize if pSize != None else 20)(pageSize)
    ret = models.LMSLS_Topic().aggregate()
    ret.match("publish == {0} and topic_approved == {1} and publish_date <= {2} and topic_removed=={3}", True, True,
              datetime.datetime.now(), False) # lấy topic publish true, đã approved, date <= ngày hệ thống
    ret.left_join(models.auth_user_info(), "created_by", "username", "uc")
    ret.left_join(models.auth_user_info(), "modified_by", "username", "um")
    ret.left_join(models.auth_user_info(), "approved_by", "username", "ua")
    ret.left_join(models.LMSLS_Forum(), "forum_id", "forum_id", "fr")



    if (where != None):
        if (where.has_key('parent_code') and (where['parent_code'] == None or where['parent_code'] == '0')): # là node cha
            if (where.has_key('forum_id') and where['forum_id'] != None): # kiểm tra id của node cha
                if(where['forum_id'] == 0 or where['forum_id'] == '0'): #lấy all topic
                    pass
                elif (where['forum_id'] == 1 or where['forum_id'] == '1'): # lấy topic của forum public
                    ret.match("(fr.forum_type=={0})", True)
                elif (where['forum_id'] == 2 or where['forum_id'] == '2'): # lấy topic của forum private
                    ret.match("(fr.forum_type=={0})", False)
        else:
            if (where.has_key('forum_id') and where['forum_id'] != None):
                ret.match("(forum_id=={0})", where['forum_id'])

    ret.project(
        topic_id=1,
        topic_name=1,
        topic_name_other=1,
        forum_id=1,
        topic_description=1,

        publish=1,
        publish_date=1,
        allow_replies=1,

        topic_replies=1,
        topic_views=1,
        approved_by="ua.login_account",
        approved_on=1,
        rejected_by=1,
        rejected_on=1,
        feedback=1,
        topic_approved=1,
        topic_removed=1,

        created_by="uc.login_account",
        created_on="created_on",
        modified_on="switch(case(modified_on!='',modified_on),'')",
        modified_by="switch(case(modified_by!='',um.login_account),'')",
    )

    if (searchText != None and searchText != ''):
        ret.match("contains(topic_name, @name) or contains(topic_description, @name)", name=searchText)

    if (sort != None):
        ret.sort(sort)

    data = ret.get_page(pageIndex, pageSize)
    return data

def get_list_with_searchtext_scheduled(args):
    searchText = args['data'].get('search', '')
    pageSize = args['data'].get('pageSize', 0)
    pageIndex = args['data'].get('pageIndex', 20)
    sort = args['data'].get('sort', 20)
    where = args['data'].get('where')

    pageIndex = (lambda pIndex: pIndex if pIndex != None else 0)(pageIndex)
    pageSize = (lambda pSize: pSize if pSize != None else 20)(pageSize)
    ret = models.LMSLS_Topic().aggregate()
    ret.match("publish == {0} and topic_approved == {1} and publish_date > {2} and topic_removed=={3}", True, True,
              datetime.datetime.now(), False) # lấy topic publish true, đã approved, date > ngày hệ thống
    ret.left_join(models.auth_user_info(), "created_by", "username", "uc")
    ret.left_join(models.auth_user_info(), "modified_by", "username", "um")
    ret.left_join(models.auth_user_info(), "approved_by", "username", "ua")
    ret.left_join(models.LMSLS_Forum(), "forum_id", "forum_id", "fr")



    if (where != None):
        if (where.has_key('parent_code') and (where['parent_code'] == None or where['parent_code'] == '0')): # là node cha
            if (where.has_key('forum_id') and where['forum_id'] != None): # kiểm tra id của node cha
                if(where['forum_id'] == 0 or where['forum_id'] == '0'): #lấy all topic
                    pass
                elif (where['forum_id'] == 1 or where['forum_id'] == '1'): # lấy topic của forum public
                    ret.match("(fr.forum_type=={0})", True)
                elif (where['forum_id'] == 2 or where['forum_id'] == '2'): # lấy topic của forum private
                    ret.match("(fr.forum_type=={0})", False)
        else:
            if (where.has_key('forum_id') and where['forum_id'] != None):
                ret.match("(forum_id=={0})", where['forum_id'])

    ret.project(
        topic_id=1,
        topic_name=1,
        topic_name_other=1,
        forum_id=1,
        topic_description=1,

        publish=1,
        publish_date=1,
        allow_replies=1,

        topic_replies=1,
        topic_views=1,
        approved_by="ua.login_account",
        approved_on=1,
        rejected_by=1,
        rejected_on=1,
        feedback=1,
        topic_approved=1,
        topic_removed=1,

        created_by="uc.login_account",
        created_on="created_on",
        modified_on="switch(case(modified_on!='',modified_on),'')",
        modified_by="switch(case(modified_by!='',um.login_account),'')",
    )

    if (searchText != None and searchText != ''):
        ret.match("contains(topic_name, @name) or contains(topic_description, @name)", name=searchText)

    if (sort != None):
        ret.sort(sort)

    data = ret.get_page(pageIndex, pageSize)
    return data

def get_list_with_searchtext_returned(args):
    searchText = args['data'].get('search', '')
    pageSize = args['data'].get('pageSize', 0)
    pageIndex = args['data'].get('pageIndex', 20)
    sort = args['data'].get('sort', 20)
    where = args['data'].get('where')

    pageIndex = (lambda pIndex: pIndex if pIndex != None else 0)(pageIndex)
    pageSize = (lambda pSize: pSize if pSize != None else 20)(pageSize)
    collection = common.get_collection('LMSLS_Topic')

    arrayData = []
    match = {}

    lookup = {
        "$lookup":
            {
                "from": common.get_collection_name_with_schema("auth_user_info"),
                "localField": 'created_by',
                "foreignField": 'username',
                "as": 'uc'
            }
    }
    arrayData.append(lookup)

    lookup = {
        "$lookup":
            {
                "from": common.get_collection_name_with_schema("auth_user_info"),
                "localField": 'modified_by',
                "foreignField": 'username',
                "as": 'um'
            }
    }
    arrayData.append(lookup)

    lookup = {
        "$lookup":
            {
                "from": common.get_collection_name_with_schema("LMSLS_Forum"),
                "localField": 'forum_id',
                "foreignField": 'forum_id',
                "as": 'fr'
            }
    }
    arrayData.append(lookup)

    lookup = {
        "$lookup":
            {
                "from": common.get_collection_name_with_schema("auth_user_info"),
                "localField": 'rejected_by',
                "foreignField": 'username',
                "as": 'ur'
            }
    }
    arrayData.append(lookup)

    arrayData.append({
        "$unwind": "$uc"
    })
    arrayData.append({
        "$unwind": "$um"
    })
    arrayData.append({
        "$unwind": "$fr"
    })
    arrayData.append({
        "$unwind": "$ur"
    })

    if (where != None):
        match = {
            "$match": qmongo.helpers.filter("expr(publish == {0} and topic_approved == {1} and (({2}-rejected_on)/86400000)<10 and topic_removed=={3})",
                                            True, False, datetime.datetime.now(), False).get_filter() # lấy topic publish true, không được approved
        }

        if (where.has_key('parent_code') and (
                where['parent_code'] == None or where['parent_code'] == '0')):  # là node cha
            if (where.has_key('forum_id') and where['forum_id'] != None):  # kiểm tra id của node cha
                if (where['forum_id'] == 0 or where['forum_id'] == '0'):  # lấy all topic
                    pass
                elif (where['forum_id'] == 1 or where['forum_id'] == '1'):  # lấy topic của forum public
                    match["$match"]["fr.forum_type"] = True
                elif (where['forum_id'] == 2 or where['forum_id'] == '2'):  # lấy topic của forum private
                    match["$match"]["fr.forum_type"] = False
        else:
            if (where.has_key('forum_id') and where['forum_id'] != None):
                match["$match"]["forum_id"] = where['forum_id']

    arrayData.append({
        "$project": {
            'topic_id': 1,
            'topic_name': 1,
            'topic_name_other': 1,
            'forum_id': 1,
            'topic_description': 1,
            'publish': 1,
            'publish_date': 1,
            'allow_replies': 1,
            'topic_replies': 1,
            'topic_views': 1,
            'approved_by': 1,
            'approved_on': 1,
            'rejected_on': 1,
            'rejected_by': "$ur.login_account",
            'topic_approved': 1,
            'feedback': 1,
            'topic_removed': 1,

            'fr': '$fr',
            'created_on': 1,
            'created_by': "$uc.login_account",
            'modified_on': 1,
            'modified_by': "$um.login_account",
        }
    })

    if (searchText != None and searchText != ''):
        arrayData.append({
            "$match": qmongo.helpers.filter("contains(topic_name, @name) or contains(topic_description, @name)",
                                            name=searchText).get_filter()
        })

    arrayData.append(match)

    if (sort != None):
        arrayData.append({
            "$sort": sort
        })
    ret = collection.aggregate(arrayData)
    return dict(
        items=list(ret),
        page_index=pageIndex,
        page_size=pageSize,
        total_items=list(ret).__len__()
    )

def get_list_with_searchtext_removed(args):

    searchText = args['data'].get('search', '')
    pageSize = args['data'].get('pageSize', 0)
    pageIndex = args['data'].get('pageIndex', 20)
    sort = args['data'].get('sort', 20)
    where = args['data'].get('where')

    pageIndex = (lambda pIndex: pIndex if pIndex != None else 0)(pageIndex)
    pageSize = (lambda pSize: pSize if pSize != None else 20)(pageSize)
    collection = common.get_collection('LMSLS_Topic')

    arrayData = []
    match = {}

    lookup = {
        "$lookup":
            {
                "from": common.get_collection_name_with_schema("auth_user_info"),
                "localField": 'created_by',
                "foreignField": 'username',
                "as": 'uc'
            }
    }
    arrayData.append(lookup)

    lookup = {
        "$lookup":
            {
                "from": common.get_collection_name_with_schema("auth_user_info"),
                "localField": 'modified_by',
                "foreignField": 'username',
                "as": 'um'
            }
    }
    arrayData.append(lookup)

    lookup = {
        "$lookup":
            {
                "from": common.get_collection_name_with_schema("LMSLS_Forum"),
                "localField": 'forum_id',
                "foreignField": 'forum_id',
                "as": 'fr'
            }
    }
    arrayData.append(lookup)

    arrayData.append({
        "$unwind": "$uc"
    })
    arrayData.append({
        "$unwind": "$um"
    })
    arrayData.append({
        "$unwind": "$fr"
    })

    if (where != None):
        match = {
            "$match": qmongo.helpers.filter("expr((({0}-rejected_on)/86400000)>10 or topic_removed=={1})", datetime.datetime.now(), True).get_filter()
        }
        if (where.has_key('parent_code') and (where['parent_code'] == None or where['parent_code'] == '0')): # là node cha
            if (where.has_key('forum_id') and where['forum_id'] != None): # kiểm tra id của node cha
                if(where['forum_id'] == 0 or where['forum_id'] == '0'): #lấy all topic
                    pass
                elif (where['forum_id'] == 1 or where['forum_id'] == '1'): # lấy topic của forum public
                    match["$match"]["fr.forum_type"] = True
                elif (where['forum_id'] == 2 or where['forum_id'] == '2'): # lấy topic của forum private
                    match["$match"]["fr.forum_type"] = False
        else:
            if (where.has_key('forum_id') and where['forum_id'] != None):
                match["$match"]["forum_id"] = where['forum_id']

    arrayData.append({
                "$project": {
                    'topic_id': 1,
                    'topic_name': 1,
                    'topic_name_other': 1,
                    'forum_id': 1,
                    'topic_description': 1,
                    'publish': 1,
                    'publish_date': 1,
                    'allow_replies': 1,
                    'topic_replies': 1,
                    'topic_views': 1,
                    'approved_by': 1,
                    'approved_on': 1,
                    'rejected_on': 1,
                    'rejected_by': 1,
                    'topic_approved': 1,
                    'feedback': 1,
                    'topic_removed': 1,

                    'fr': '$fr',
                    'created_on': 1,
                    'created_by': "$uc.login_account",
                    'modified_on': 1,
                    'modified_by': "$um.login_account"
                }
            })

    if (searchText != None and searchText != ''):
        arrayData.append({
            "$match": qmongo.helpers.filter("contains(topic_name, @name) or contains(topic_description, @name)", name=searchText).get_filter()
        })

    arrayData.append(match)

    if (sort != None):
        arrayData.append({
            "$sort": sort
        })
    ret = collection.aggregate(arrayData)
    return dict(
        items=list(ret),
        page_index=pageIndex,
        page_size=pageSize,
        total_items=list(ret).__len__()
    )

def get_list_with_searchtext_all(args):
    searchText = args['data'].get('search', '')
    pageSize = args['data'].get('pageSize', 0)
    pageIndex = args['data'].get('pageIndex', 20)
    sort = args['data'].get('sort', 20)
    where = args['data'].get('where')

    pageIndex = (lambda pIndex: pIndex if pIndex != None else 0)(pageIndex)
    pageSize = (lambda pSize: pSize if pSize != None else 20)(pageSize)
    collection = common.get_collection('LMSLS_Topic')

    arrayData = []
    match = {}

    lookup = {
        "$lookup":
            {
                "from": common.get_collection_name_with_schema("auth_user_info"),
                "localField": 'created_by',
                "foreignField": 'username',
                "as": 'uc'
            }
    }
    arrayData.append(lookup)

    lookup = {
        "$lookup":
            {
                "from": common.get_collection_name_with_schema("auth_user_info"),
                "localField": 'modified_by',
                "foreignField": 'username',
                "as": 'um'
            }
    }
    arrayData.append(lookup)

    lookup = {
        "$lookup":
            {
                "from": common.get_collection_name_with_schema("LMSLS_Forum"),
                "localField": 'forum_id',
                "foreignField": 'forum_id',
                "as": 'fr'
            }
    }
    arrayData.append(lookup)

    arrayData.append({
        "$unwind": "$uc"
    })
    arrayData.append({"$unwind": {'path': '$um', "preserveNullAndEmptyArrays": True}})

    arrayData.append({
        "$unwind": "$fr"
    })

    if (where != None):
        match = {
            "$match": {}
        }
        if (where.has_key('parent_code') and (where['parent_code'] == None or where['parent_code'] == '0')):  # là node cha
            if (where.has_key('forum_id') and where['forum_id'] != None):  # kiểm tra id của node cha
                if (where['forum_id'] == 0 or where['forum_id'] == '0'):  # lấy all topic
                    pass
                elif (where['forum_id'] == 1 or where['forum_id'] == '1'):  # lấy topic của forum public
                    match["$match"]["fr.forum_type"] = True
                elif (where['forum_id'] == 2 or where['forum_id'] == '2'):  # lấy topic của forum private
                    match["$match"]["fr.forum_type"] = False
        else:
            if (where.has_key('forum_id') and where['forum_id'] != None):
                match["$match"]["forum_id"] = where['forum_id']

    arrayData.append({
        "$project": {
            'topic_id': 1,
            'topic_name': 1,
            'topic_name_other': 1,
            'forum_id': 1,
            'topic_description': 1,
            'publish': 1,
            'publish_date': 1,
            'allow_replies': 1,
            'topic_replies': 1,
            'topic_views': 1,
            'approved_by': 1,
            'rejected_on': 1,
            'rejected_by': 1,
            'topic_approved': 1,
            'feedback': 1,
            'topic_removed': 1,

            'created_on': 1,
            'created_by': "$uc.login_account",
            'fr': '$fr',
            'modified_on': 1,
            'modified_by': {"$ifNull": ["$um.login_account", ""]},
            'status':
                {"$cond": {
                    "if": {
                        "$and": [
                            {"$eq": ["$publish", False]},
                            {"$eq": ["$topic_removed", False]}
                        ]
                    },
                    "then": 1,
                    "else": {
                        "$cond": {
                            "if": {
                                "$and": [
                                    {"$eq": ["$publish", True]},
                                    {"$eq": ["$topic_approved", None]},
                                    {"$eq": ["$topic_removed", False]}
                                ]
                            },
                            "then": 2,
                            "else": {
                                "$cond": {
                                    "if": {
                                        "$and": [
                                            {"$eq": ["$publish", True]},
                                            {"$eq": ["$topic_approved", True]},
                                            {"$eq": ["$topic_removed", False]},
                                            {"$lte": [
                                                {"$subtract": ["$publish_date", datetime.datetime.now()]},
                                                1000 * 60 * 60 * 24
                                            ]}
                                        ]

                                    },
                                    "then": 3,
                                    "else": {
                                        "$cond": {
                                            "if": {
                                                "$and": [
                                                    {"$eq": ["$publish", True]},
                                                    {"$eq": ["$topic_approved", True]},
                                                    {"$eq": ["$topic_removed", False]},
                                                    {"$gt": [
                                                        {"$subtract": ["$publish_date", datetime.datetime.now()]},
                                                        1000 * 60 * 60 * 24
                                                    ]}
                                                ]

                                            },
                                            "then": 4,
                                            "else": {
                                                "$cond": {
                                                    "if": {
                                                        "$and": [
                                                            {"$eq": ["$publish", True]},
                                                            {"$eq": ["$topic_approved", False]},
                                                            {"$eq": ["$topic_removed", False]},
                                                            {"$lt": [
                                                                {"$subtract": [datetime.datetime.now(), "$rejected_on"]},
                                                                10 * 1000 * 60 * 60 * 24
                                                            ]}
                                                        ]

                                                    },
                                                    "then": 5,
                                                    "else": {
                                                        "$cond": {
                                                            "if": {
                                                                "$or": [
                                                                    {"$eq": ["$topic_removed", True]},
                                                                    {"$gt": [
                                                                        {"$subtract": [datetime.datetime.now(), "$rejected_on"]},
                                                                        10 * 1000 * 60 * 60 * 24
                                                                    ]}
                                                                ]

                                                            },
                                                            "then": 6,
                                                            "else": "false"
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }

                    }
                }
            },
        }
    })

    arrayData.append(match)

    if (searchText != None and searchText != ''):
        arrayData.append({
            "$match": qmongo.helpers.filter("contains(topic_name, @name) or contains(topic_description, @name)",
                                            name=searchText).get_filter()
        })

    if (sort != None):
        arrayData.append({
            "$sort": sort
        })
    ret = collection.aggregate(arrayData)
    return dict(
        items=list(ret),
        page_index=pageIndex,
        page_size=pageSize,
        total_items=list(ret).__len__()
    )

def insert(args):
    try:
        lock.acquire()
        ret = {}
        if args['data'] != None:
            data = set_dict_insert_data(args)
            ret = models.LMSLS_Topic().insert(data)
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
            data = set_dict_update_data(args)

            if args['data']['topic_approved'] == False:
                set_dict_reject(data)
            elif args['data']['topic_approved'] == True:
                set_dict_approve(data)

            ret = models.LMSLS_Topic().update(
                data,
                "_id == {0}",
                ObjectId(args['data']['_id']))
            if ret.has_key('data') and ret['data'].raw_result['updatedExisting'] == True:
                ret.update(
                    item=get_list_data().match("_id == {0}", ObjectId(args['data']['_id'])).get_item()
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
            ret = models.LMSLS_Topic().delete("_id in {0}", [ObjectId(x["_id"]) for x in args['data']])
            lock.release()
            return ret

        lock.release()
        return dict(
            error="request parameter is not exist"
        )
    except Exception as ex:
        lock.release()
        raise (ex)

def delete_to_trash(args):
    try:
        lock.acquire()
        ret = {}

        if args['data'] != None:
            for el in args['data']:
                ret = models.LMSLS_Topic().update(
                    {
                        "topic_removed": True
                    },
                    "_id == {0}",
                    ObjectId(el["_id"]))

            lock.release()
            return ret

        lock.release()
        return dict(
            error="request parameter is not exist"
        )
    except Exception as ex:
        lock.release()
        raise (ex)

def update_topic_pin(args):
    try:
        lock.acquire()
        ret = {}

        if args['data'] != None:
            for el in args['data']:
                ret = models.LMSLS_Topic().update(
                    {
                        "topic_pin": True
                    },
                    "_id == {0}",
                    ObjectId(el["_id"]))

            lock.release()
            return ret

        lock.release()
        return dict(
            error="request parameter is not exist"
        )
    except Exception as ex:
        lock.release()
        raise (ex)

def update_topic_block(args):
        try:
            lock.acquire()
            ret = {}

            if args['data'] != None:
                for el in args['data']:
                    ret = models.LMSLS_Topic().update(
                        {
                            "topic_block": True
                        },
                        "_id == {0}",
                        ObjectId(el["_id"]))

                lock.release()
                return ret

            lock.release()
            return dict(
                error="request parameter is not exist"
            )
        except Exception as ex:
            lock.release()
            raise (ex)

def set_dict_insert_data(args):
    ret_dict = dict()

    ret_dict.update(
        topic_id=(lambda x: x['topic_id'] if x.has_key('topic_id') else None)(args['data']),
        topic_name=(lambda x: x['topic_name'] if x.has_key('topic_name') else None)(args['data']),
        topic_name_other=(lambda x: x['topic_name_other'] if x.has_key('topic_name_other') else None)(args['data']),
        forum_id=(lambda x: x['forum_id'] if x.has_key('forum_id') else None)(args['data']),
        topic_description=(lambda x: x['topic_description'] if x.has_key('topic_description') else None)(args['data']),

        publish=(lambda x: x['publish'] if x.has_key('publish') else None)(args['data']),
        publish_date=(lambda x: x['publish_date'] if x.has_key('publish_date') else None)(args['data']),
        allow_replies=(lambda x: x['allow_replies'] if x.has_key('allow_replies') else None)(args['data']),

        topic_replies=(lambda x: x['topic_replies'] if x.has_key('topic_replies') else None)(args['data']),
        topic_views=(lambda x: x['topic_views'] if x.has_key('topic_views') else None)(args['data']),
        approved_by=(lambda x: x['approved_by'] if x.has_key('approved_by') else None)(args['data']),
        rejected_by=(lambda x: x['rejected_by'] if x.has_key('rejected_by') else None)(args['data']),
        rejected_on=(lambda x: x['rejected_on'] if x.has_key('rejected_on') else None)(args['data']),
        feedback=(lambda x: x['feedback'] if x.has_key('feedback') else None)(args['data']),
        topic_approved=(lambda x: x['topic_approved'] if x.has_key('topic_approved') else None)(args['data']),
        topic_removed=(lambda x: x['topic_removed'] if x.has_key('topic_removed') else None)(args['data']),
        topic_pin=(lambda x: x['topic_pin'] if x.has_key('topic_pin') else None)(args['data']),
        topic_block=(lambda x: x['topic_block'] if x.has_key('topic_block') else None)(args['data']),
    )

    return ret_dict

def set_dict_update_data(args):
    ret_dict = set_dict_insert_data(args)
    del ret_dict['topic_id']
    return ret_dict

def set_dict_reject(data):

    data.update(
        rejected_by=common.get_user_id(),
        rejected_on=datetime.datetime.now()
    )

    return data

def set_dict_approve(data):

    data.update(
        approved_by=common.get_user_id(),
        approved_on=datetime.datetime.now()
    )

    return data
