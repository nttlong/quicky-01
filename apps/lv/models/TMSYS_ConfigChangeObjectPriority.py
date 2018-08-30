# -*- coding: utf-8 -*-
from config import database, helpers, db_context
import datetime
import base
import threading
helpers.extent_model(
            "TMSYS_ConfigChangeObjectPriority",
            "base",
            [[]],
            value_list_key = ('text'),
            change_object = ('numeric'),
            change_object_name = ('text'),
            priority_no = ('numeric'),
            table_name = ('text'),
            note = ('text'),
            language = ('numeric'),
            created_on=("date"),
            created_by=("text"),
            modified_on=("date"),
            modified_by=("text")
        )
def TMSYS_ConfigChangeObjectPriority():
    ret = db_context.collection("TMSYS_ConfigChangeObjectPriority")
    return ret