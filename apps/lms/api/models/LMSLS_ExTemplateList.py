# -*- coding: utf-8 -*-
from config import database, helpers, db_context
_hasCreated=False
helpers.extent_model(
            "LMSLS_ExTemplateList",
            "base",
            [["exam_temp_id"]],
            exam_temp_id=helpers.create_field("text", True),
            exam_temp_category=helpers.create_field("text", True),
            exam_temp_name1=helpers.create_field("text",True),
            exam_temp_name2=helpers.create_field("text"),
            duration=helpers.create_field("text"),
            negative_marks=helpers.create_field("text"),
            mode_pick =helpers.create_field("text"),
            creator = helpers.create_field("text"),
            question_list=helpers.create_field("list"),
            total_question = helpers.create_field("numeric"),
            total_mask = helpers.create_field("numeric"),
            easy_question = helpers.create_field("text"),
            med_question = helpers.create_field("text"),
            diff_question = helpers.create_field("text"),
        )
def LMSLS_ExTemplateList():
    global _hasCreated
    if not _hasCreated:
        _hasCreated=True
    ret = db_context.collection("LMSLS_ExTemplateList")

    return ret