# -*- coding: utf-8 -*-
from config import database, helpers, db_context
import datetime
import base
import threading
helpers.extent_model(
            "HCSLS_Award",
            "base",
            [["award_code"]],
            award_code = ("text", True),
            award_name = ("text", True),
            award_name2 = ("text"),
            ordinal = ("numeric"),
            note = ("text"),
            lock=("bool"),
            award_level_code=("text"),
            award_place_code = ("text"),
            award_type = ("numeric"),
            is_team = ("bool"),
            created_on=("date"),
            created_by=("text"),
            modified_on=("date"),
            modified_by=("text")
        )
def HCSLS_Award():
    ret = db_context.collection("HCSLS_Award")
    return ret