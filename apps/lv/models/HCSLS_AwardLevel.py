# -*- coding: utf-8 -*-
from config import database, helpers, db_context
import datetime
import base
import threading
helpers.extent_model(
            "HCSLS_AwardLevel",
            "base",
            [["award_level_code"]],
            award_level_code = ("text", True),
            award_level_name = ("text", True),
            award_level_name2 = ("text"),
            ordinal = ("numeric"),
            note = ("text"),
            lock=("bool"),
            max_times_per_year=("numeric"),
            created_on=("date"),
            created_by=("text"),
            modified_on=("date"),
            modified_by=("text")
        )
def HCSLS_AwardLevel():
    ret = db_context.collection("HCSLS_AwardLevel")
    return ret