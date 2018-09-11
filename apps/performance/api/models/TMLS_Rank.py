# -*- coding: utf-8 -*-
from config import database, helpers, db_context
import datetime
import base
import threading
helpers.extent_model(
            "TMLS_Rank",
            "base",
            [["rank_code"]],
            rank_code = ('text', True),
            rank_name = ('text', True),
            rank_name2 = ('text'),
            rank_content = ('text'),
            total_from = ('numeric'),
            total_to = ('numeric'),
            is_change_object = ('bool'),
            ordinal = ('numeric'),
            lock = ('bool'),
            created_on=("date"),
            created_by=("text"),
            modified_on=("date"),
            modified_by=("text"),
            #TMLS_RankSub
            details=("list",False,dict(
                rec_id = ('text'),# True),
                rank_code = ('text'),# True),
                change_object = ('numeric'),# True),
                object_level = ('numeric'),
                object_code = ('text'),# True),
                object_name = ('text'),
                priority_no = ('numeric'),
                total_from = ('numeric'),
                total_to = ('numeric'),
                note = ('text'),
                created_on=("date"),
                created_by=("text"),
                modified_on=("date"),
                modified_by=("text")
            ))
        )
def TMLS_Rank():
    ret = db_context.collection("TMLS_Rank")
    return ret