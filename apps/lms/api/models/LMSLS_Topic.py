# -*- coding: utf-8 -*-
from config import database, helpers, db_context
from ...api import common

import datetime
_hasCreated=False
helpers.extent_model(
            "LMSLS_Topic",
            "base",
            [['topic_id']],
            topic_id=helpers.create_field("text", True),
            topic_name=helpers.create_field("text", True),
            topic_name_other=helpers.create_field("text"),
            forum_id=helpers.create_field("text"),
            topic_description=helpers.create_field("text"),

            publish=helpers.create_field("bool"),
            publish_date=helpers.create_field("date"),
            allow_replies=helpers.create_field("bool"),

            topic_replies=helpers.create_field("numberic"),
            topic_views=helpers.create_field("numberic"),
            approved_by=helpers.create_field("text"),
            approved_on=helpers.create_field("date"),
            rejected_by=helpers.create_field("text"),
            rejected_on=helpers.create_field("date"),
            feedback=helpers.create_field("text"),
            topic_approved=helpers.create_field("bool"),
            topic_removed=helpers.create_field("bool"),
            topic_pin=helpers.create_field("bool"),
            topic_block=helpers.create_field("bool"),


            created_on=helpers.create_field("date"),
            created_by=helpers.create_field("text"),
            modified_on=helpers.create_field("date"),
            modified_by=helpers.create_field("text"),
        )
def on_before_insert(data):
    pass

def on_before_update(data):
    pass

helpers.events("LMSLS_Topic").on_before_insert(on_before_insert).on_before_update(on_before_update)
def LMSLS_Topic():
    ret = db_context.collection("LMSLS_Topic")
    return ret
