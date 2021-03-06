# -*- coding: utf-8 -*-
from config import database, helpers, db_context
from ...api import common

import datetime
_hasCreated=False
helpers.extent_model(
            "LMSLS_Forum",
            "base",
            [['forum_id']],
            forum_id=helpers.create_field("text", True),
            forum_name=helpers.create_field("text", True),
            forum_name_other=helpers.create_field("text"),
            description=helpers.create_field("text"),
            forum_type=helpers.create_field("bool"),
            info_course_name=helpers.create_field("text"),
            info_start_date=helpers.create_field("date"),
            info_class_code=helpers.create_field("text"),

            forum_avail=helpers.create_field("bool"),
            avail_start_date=helpers.create_field("date"),
            avail_end_date=helpers.create_field("date"),
            avail=helpers.create_field("object"),
            allow_anonymous_posts=helpers.create_field("bool"),
            allow_attachment_files=helpers.create_field("bool"),
            limit_space=float,
            max_number_posts=helpers.create_field("text"),

            allow_author_delete=float,
            allow_author_edit=helpers.create_field("bool"),
            allow_post_tagging=helpers.create_field("bool"),
            allow_user_reply=helpers.create_field("bool"),
            allow_member_thread=helpers.create_field("bool"),

            subscription_type=helpers.create_field("bool"),
            allow_member_rate=helpers.create_field("bool"),
            force_moderation_post=helpers.create_field("bool"),
            type_moderation=float,
            forum_administrator=helpers.create_field("text"),
            forum_status=float,
            disable=helpers.create_field("bool"),
            order=float,

            created_on=helpers.create_field("date"),
            created_by=helpers.create_field("text"),
            modified_on=helpers.create_field("date"),
            modified_by=helpers.create_field("text"),
        )
def on_before_insert(data):
    pass

def on_before_update(data):
    pass

helpers.events("LMSLS_Forum").on_before_insert(on_before_insert).on_before_update(on_before_update)
def LMSLS_Forum():
    ret = db_context.collection("LMSLS_Forum")
    return ret
