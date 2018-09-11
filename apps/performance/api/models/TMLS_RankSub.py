# -*- coding: utf-8 -*-
from config import database, helpers, db_context
import datetime
import base
import threading
helpers.extent_model(
            "TMLS_RankSub",
            "base",
            [["rank_code"]],
            rec_id = ('text'),
            rank_code = ('text'),
            change_object = ('numeric'),
            object_level = ('numeric'),
            object_code = ('text'),
            object_name = ('text'),
            priority_no = ('numeric'),
            total_from = ('numeric'),
            total_to = ('numeric'),
            created_on=("date"),
            created_by=("text"),
            modified_on=("date"),
            modified_by=("text")
        )
def TMLS_RankSub():
    ret = db_context.collection("TMLS_RankSub")
    return ret