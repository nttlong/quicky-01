# -*- coding: utf-8 -*-
from bson import ObjectId
import qmongo
import models
import logging
import threading
import common
import random
import datetime

logger = logging.getLogger(__name__)
global lock
lock = threading.Lock()
import qmongo
def get_list_tree_data(args):
    items =qmongo.models.LMSLS_Forum.aggregate
    items.match("forum_type=={0}", True).project(
        forum_id=1,
        forum_name=1,
    )
    data = items.get_list()
    data_public_forum = [parent_public_forum(x) for x in data]

    items = qmongo.models.LMSLS_Forum.aggregate
    items.match("forum_type=={0}", False).project(
        forum_id=1,
        forum_name=1,
    )
    data = items.get_list()
    data_private_forum = [parent_private_forum(x) for x in data]



    return dict(
        data=sum([data_public_forum, data_private_forum], [])
    )

def parent_public_forum (arg):
    arg['parent_code'] = 1
    return arg

def parent_private_forum (arg):
    arg['parent_code'] = 2
    return arg

def get_list_data():
    items =qmongo.models.LMSLS_Forum.aggregate
    items.left_join(qmongo.models.auth_user_info, "created_by", "username", "uc")
    items.left_join(qmongo.models.auth_user_info, "modified_by", "username", "um")
    items.project(
        forum_id=1,
        forum_name=1,
        forum_name_other=1,
        description=1,
        forum_type=1,
        info_course_name=1,
        info_start_date=1,
        info_class_code=1,

        forum_avail=1,
        avail=1,
        avail_start_date=1,
        avail_end_date=1,
        allow_anonymous_posts=1,
        allow_attachment_files=1,
        limit_space=1,
        max_number_posts=1,

        allow_author_delete=1,
        allow_author_edit=1,
        allow_post_tagging=1,
        allow_user_reply=1,
        allow_member_thread=1,

        subscription_type=1,
        allow_member_rate=1,
        force_moderation_post=1,
        type_moderation=1,
        forum_administrator=1,
        forum_status=1,
        disable=1,
        order=1,

        created_by="uc.login_account",
        created_on="created_on",
        modified_on="switch(case(modified_on!='',modified_on),'')",
        modified_by="switch(case(modified_by!='',um.login_account),'')",
    )

    return items

def get_list_with_searchtext_public(args):
    searchText = args['data'].get('search', '')
    pageSize = args['data'].get('pageSize', 0)
    pageIndex = args['data'].get('pageIndex', 20)
    sort = args['data'].get('sort', 20)
    where = args['data'].get('where')

    pageIndex = (lambda pIndex: pIndex if pIndex != None else 0)(pageIndex)
    pageSize = (lambda pSize: pSize if pSize != None else 20)(pageSize)

    ret =  qmongo.models.LMSLS_Forum.aggregate
    ret.lookup(qmongo.views.LMS_VW_Employee, "forum_administrator", "employee_code", "emp")
    ret.unwind("emp", True)
    ret.match("(forum_type=={0})", True)
    ret.project(
        forum_id=1,
        forum_name=1,
        forum_name_other=1,
        description=1,
        forum_type=1,
        info_course_name=1,
        info_start_date=1,
        info_class_code=1,

        forum_avail=1,
        avail=1,
        avail_start_date=1,
        avail_end_date=1,

        allow_anonymous_posts=1,
        allow_attachment_files=1,
        limit_space=1,
        max_number_posts=1,

        allow_author_delete=1,
        allow_author_edit=1,
        allow_post_tagging=1,
        allow_user_reply=1,
        allow_member_thread=1,

        subscription_type=1,
        allow_member_rate=1,
        force_moderation_post=1,
        type_moderation=1,
        forum_administrator=1,
        forum_administrator_name="concat(emp.last_name, ' ', emp.first_name)",
        forum_status=1,
        disable=1,
        order=1,

        created_on=1,
        created_by=1,
        modified_on=1,
        modified_by=1,
    )

    if (searchText != None and searchText != ''):
        ret.match("contains(forum_name, @name) or contains(forum_description, @name)", name=searchText)

    if (sort != None):
        ret.sort(sort)

    data = ret.get_page(pageIndex, pageSize)
    return data

def get_list_with_searchtext_private(args):
    searchText = args['data'].get('search', '')
    pageSize = args['data'].get('pageSize', 0)
    pageIndex = args['data'].get('pageIndex', 20)
    sort = args['data'].get('sort', 20)
    where = args['data'].get('where')

    pageIndex = (lambda pIndex: pIndex if pIndex != None else 0)(pageIndex)
    pageSize = (lambda pSize: pSize if pSize != None else 20)(pageSize)
    ret = qmongo.models.LMSLS_Forum.aggregate
    ret.lookup(qmongo.views.LMS_VW_Employee, "forum_administrator", "employee_code", "emp")
    ret.unwind("emp", True)
    ret.match("(forum_type=={0})", False)
    ret.project(
        forum_id=1,
        forum_name=1,
        forum_name_other=1,
        description=1,
        forum_type=1,
        info_course_name=1,
        info_start_date=1,
        info_class_code=1,

        forum_avail=1,
        avail=1,
        avail_start_date=1,
        avail_end_date=1,

        allow_anonymous_posts=1,
        allow_attachment_files=1,
        limit_space=1,
        max_number_posts=1,

        allow_author_delete=1,
        allow_author_edit=1,
        allow_post_tagging=1,
        allow_user_reply=1,
        allow_member_thread=1,

        subscription_type=1,
        allow_member_rate=1,
        force_moderation_post=1,
        type_moderation=1,
        forum_administrator=1,
        forum_administrator_name="concat(emp.last_name, ' ', emp.first_name)",
        forum_status=1,
        disable=1,
        order=1,

        created_on=1,
        created_by=1,
        modified_on=1,
        modified_by=1,
    )

    if (searchText != None and searchText != ''):
        ret.match("contains(forum_name, @name) or contains(forum_description, @name)", name=searchText)

    if (sort != None):
        ret.sort(sort)

    data = ret.get_page(pageIndex, pageSize)
    return data

def get_list_with_searchtext_all(args):
    searchText = args['data'].get('search', '')
    pageSize = args['data'].get('pageSize', 0)
    pageIndex = args['data'].get('pageIndex', 20)
    sort = args['data'].get('sort', 20)
    where = args['data'].get('where')

    pageIndex = (lambda pIndex: pIndex if pIndex != None else 0)(pageIndex)
    pageSize = (lambda pSize: pSize if pSize != None else 20)(pageSize)
    ret = qmongo.models.LMSLS_Forum.aggregate
    ret.lookup(qmongo.views.LMS_VW_Employee, "forum_administrator", "employee_code", "emp")
    ret.unwind("emp", True)
    ret.project(
        forum_id=1,
        forum_name=1,
        forum_name_other=1,
        description=1,
        forum_type=1,
        info_course_name=1,
        info_start_date=1,
        info_class_code=1,

        forum_avail=1,
        avail=1,
        avail_start_date=1,
        avail_end_date=1,

        allow_anonymous_posts=1,
        allow_attachment_files=1,
        limit_space=1,
        max_number_posts=1,

        allow_author_delete=1,
        allow_author_edit=1,
        allow_post_tagging=1,
        allow_user_reply=1,
        allow_member_thread=1,

        subscription_type=1,
        allow_member_rate=1,
        force_moderation_post=1,
        type_moderation=1,
        forum_administrator=1,
        forum_administrator_name="concat(emp.last_name, ' ', emp.first_name)",
        forum_status=1,
        disable=1,
        order=1,

        created_on=1,
        created_by=1,
        modified_on=1,
        modified_by=1,
    )

    if (searchText != None and searchText != ''):
        ret.match("contains(forum_name, @name) or contains(description, @name)", name=searchText)

    if (sort != None):
        ret.sort(sort)

    data = ret.get_page(pageIndex, pageSize)
    return data

def get_list_with_searchtext_archived(args):
    searchText = args['data'].get('search', '')
    pageSize = args['data'].get('pageSize', 0)
    pageIndex = args['data'].get('pageIndex', 20)
    sort = args['data'].get('sort', 20)
    where = args['data'].get('where')

    pageIndex = (lambda pIndex: pIndex if pIndex != None else 0)(pageIndex)
    pageSize = (lambda pSize: pSize if pSize != None else 20)(pageSize)
    ret = qmongo.models.LMSLS_Forum.aggregate
    ret.lookup(qmongo.views.LMS_VW_Employee, "forum_administrator", "employee_code", "emp")
    ret.unwind("emp", True)
    ret.match("(avail_end_date<{0})", datetime.datetime.now())
    ret.project(
        forum_id=1,
        forum_name=1,
        forum_name_other=1,
        description=1,
        forum_type=1,
        info_course_name=1,
        info_start_date=1,
        info_class_code=1,

        forum_avail=1,
        avail=1,
        avail_start_date=1,
        avail_end_date=1,

        allow_anonymous_posts=1,
        allow_attachment_files=1,
        limit_space=1,
        max_number_posts=1,

        allow_author_delete=1,
        allow_author_edit=1,
        allow_post_tagging=1,
        allow_user_reply=1,
        allow_member_thread=1,

        subscription_type=1,
        allow_member_rate=1,
        force_moderation_post=1,
        type_moderation=1,
        forum_administrator=1,
        forum_administrator_name="concat(emp.last_name, ' ', emp.first_name)",
        forum_status=1,

        created_on=1,
        created_by=1,
        modified_on=1,
        modified_by=1,
    )

    if (searchText != None and searchText != ''):
        ret.match("contains(forum_name, @name) or contains(forum_description, @name)", name=searchText)

    if (sort != None):
        ret.sort(sort)

    data = ret.get_page(pageIndex, pageSize)
    return data

def insert(args):
    try:
        lock.acquire()
        ret = {}
        if args['data'] != None:
            data = set_dict_insert_data(args)
            ret =qmongo.models.LMSLS_Forum.insert(data)
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
            ret =qmongo.models.LMSLS_Forum.update(
                data,
                "_id == {0}",
                ObjectId(args['data']['_id']))
            if ret['data'].raw_result['updatedExisting'] == True:
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

def update_status_open(args):
    try:
        lock.acquire()
        ret = {}

        if args['data'] != None:
            for el in args['data']:
                ret = qmongo.models.LMSLS_Forum.update(
                    {
                        "forum_status": 1
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

def update_status_suspend(args):
        try:
            lock.acquire()
            ret = {}

            if args['data'] != None:
                for el in args['data']:
                    ret =qmongo.models.LMSLS_Forum.update(
                        {
                            "forum_status": 2
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

def update_status_write_protected(args):
            try:
                lock.acquire()
                ret = {}

                if args['data'] != None:
                    for el in args['data']:
                        ret =qmongo.models.LMSLS_Forum.update(
                            {
                                "forum_status": 3
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

def delete(args):
    try:
        lock.acquire()
        ret = {}
        if args['data'] != None:
            ret =qmongo.models.LMSLS_Forum.delete("_id in {0}", [ObjectId(x["_id"]) for x in args['data']])
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
        forum_id=(lambda x: x['forum_id'] if x.has_key('forum_id') else None)(args['data']),
        forum_name=(lambda x: x['forum_name'] if x.has_key('forum_name') else None)(args['data']),
        forum_name_other=(lambda x: x['forum_name_other'] if x.has_key('forum_name_other') else None)(args['data']),
        description=(lambda x: x['description'] if x.has_key('description') else None)(args['data']),
        forum_type=(lambda x: x['forum_type'] if x.has_key('forum_type') else None)(args['data']),
        info_course_name=(lambda x: x['info_course_name'] if x.has_key('info_course_name') else None)(args['data']),
        info_start_date=(lambda x: x['info_start_date'] if x.has_key('info_start_date') else None)(args['data']),
        info_class_code=(lambda x: x['info_class_code'] if x.has_key('info_class_code') else None)(args['data']),

        forum_avail=(lambda x: x['forum_avail'] if x.has_key('forum_avail') else None)(args['data']),
        avail=(lambda x: x['avail'] if x.has_key('avail') else None)(args['data']),
        avail_start_date=(lambda x: x['avail_start_date'] if x.has_key('avail_start_date') else None)(args['data']),
        avail_end_date=(lambda x: x['avail_end_date'] if x.has_key('avail_end_date') else None)(args['data']),
        allow_anonymous_posts=(lambda x: x['allow_anonymous_posts'] if x.has_key('allow_anonymous_posts') else None)(args['data']),
        allow_attachment_files=(lambda x: x['allow_attachment_files'] if x.has_key('allow_attachment_files') else None)(args['data']),
        limit_space=(lambda x: x['limit_space'] if x.has_key('limit_space') else None)(args['data']),
        max_number_posts=(lambda x: x['max_number_posts'] if x.has_key('max_number_posts') else None)(args['data']),

        allow_author_delete=(lambda x: x['allow_author_delete'] if x.has_key('allow_author_delete') else None)(args['data']),
        allow_author_edit=(lambda x: x['allow_author_edit'] if x.has_key('allow_author_edit') else None)(args['data']),
        allow_post_tagging=(lambda x: x['allow_post_tagging'] if x.has_key('allow_post_tagging') else None)(args['data']),
        allow_user_reply=(lambda x: x['allow_user_reply'] if x.has_key('allow_user_reply') else None)(args['data']),
        allow_member_thread=(lambda x: x['allow_member_thread'] if x.has_key('allow_member_thread') else None)(args['data']),

        subscription_type=(lambda x: x['subscription_type'] if x.has_key('subscription_type') else None)(args['data']),
        allow_member_rate=(lambda x: x['allow_member_rate'] if x.has_key('allow_member_rate') else None)(args['data']),
        force_moderation_post=(lambda x: x['force_moderation_post'] if x.has_key('force_moderation_post') else None)(args['data']),
        type_moderation=(lambda x: x['type_moderation'] if x.has_key('type_moderation') else None)(args['data']),
        forum_administrator=(lambda x: x['forum_administrator'] if x.has_key('forum_administrator') else None)(args['data']),
        forum_status=(lambda x: x['forum_status'] if x.has_key('forum_status') else None)(args['data']),
        disable=(lambda x: x['disable'] if x.has_key('disable') else None)(args['data']),
        order=(lambda x: x['order'] if x.has_key('order') else None)(args['data']),
    )

    return ret_dict

def set_dict_update_data(args):
    ret_dict = set_dict_insert_data(args)
    del ret_dict['forum_id']
    return ret_dict

