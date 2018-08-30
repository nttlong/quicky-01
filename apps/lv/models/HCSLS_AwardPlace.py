# -*- coding: utf-8 -*-
from config import database, helpers, db_context
import datetime
import base
import threading
helpers.extent_model(
            "HCSLS_AwardPlace",
            "base",
            [["award_place_code"]],
            award_place_code = ("text", True),
            award_place_name = ("text", True),
            award_place_name2 = ("text"),
            ordinal = ("numeric"),
            note = ("text"),
            lock=("bool"),
            created_on=("date"),
            created_by=("text"),
            modified_on=("date"),
            modified_by=("text")
        )
def HCSLS_AwardPlace():
    ret = db_context.collection("HCSLS_AwardPlace")
    return ret