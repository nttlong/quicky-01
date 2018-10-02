# -*- coding: utf-8 -*-
from config import database, helpers, db_context
helpers.extent_model(
            "LMSLS_PrivateForum",
            "base",
            [["pr_forum_id"]],
            pr_forum_id=("text", True),
            pr_forum_name=("text", True),
            pr_forum_description=("text"),
            pr_forum_course_name=("text"),
            pr_forum_start_date=("date"),
            pr_forum_end_date=("date"),
            pr_forum_admin=("text"),
            pr_forum_status=("text"),
        )
def LMSLS_PrivateForum():
    ret = db_context.collection("LMSLS_PrivateForum")
    return ret