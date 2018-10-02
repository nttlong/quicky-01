# -*- coding: utf-8 -*-
from config import database, helpers, db_context
_hasCreated=False
def LMSLS_ExResultType():
    global _hasCreated
    if not _hasCreated:
        helpers.extent_model(
            "LMSLS_ExResultType",
            "base",
            [["result_type_id"]],
            result_type_id=helpers.create_field("text", True),
            result_type1=helpers.create_field("text", True),
            result_type2=helpers.create_field("text"),
            grading_scale=helpers.create_field("list"),
            order=helpers.create_field("numeric"),
            note=helpers.create_field("text"),
            active=helpers.create_field("bool"),
            created_on=helpers.create_field("date"),
            creator = helpers.create_field("text"),
            created_by=helpers.create_field("text"),
            modified_on=helpers.create_field("date"),
            modified_by=helpers.create_field("text"),
        )
        _hasCreated=True
    ret = db_context.collection("LMSLS_ExResultType")

    return ret