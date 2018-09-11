# -*- coding: utf-8 -*-
from config import database, helpers, db_context
import datetime
import base
import threading
helpers.extent_model(
            "HCSLS_JobWorkingGroup",
            "base",
            [["gjw_code"]],
            gjw_code=("text", True),
            gjw_name=("text", True),
            gjw_name2=("text"),
            level_code=("list"),
            parent_code=("text"),
            level=("numeric"),
            ordinal=("numeric"),
            note=("text"),
            lock=("bool"),
            created_on=("date"),
            created_by=("text"),
            modified_on=("date"),
            modified_by=("text")
        )
def HCSLS_JobWorkingGroup():
    ret = db_context.collection("HCSLS_JobWorkingGroup")
    return ret