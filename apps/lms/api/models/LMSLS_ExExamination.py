# -*- coding: utf-8 -*-
from config import database, helpers, db_context
_hasCreated=False
def LMSLS_ExExamination():
    global _hasCreated
    if not _hasCreated:
        helpers.extent_model(
            "LMSLS_ExExamination",
            "base",
            [["exam_id"]],
            exam_id=helpers.create_field("text", True),
            exam_name1=helpers.create_field("text", True),
            exam_name2=helpers.create_field("text"),
            course_related=helpers.create_field("bool"),
            course_info=helpers.create_field("object"),
            exam_avail=helpers.create_field("bool"),
            specific_avail=helpers.create_field("object"),
            exam_mode=helpers.create_field("bool"),
            exam_form=helpers.create_field("bool"),
            who_take_exam =helpers.create_field("list"),
            assign_candidate = helpers.create_field("text"),
            choose_from=helpers.create_field("bool"),
            mode_pick = helpers.create_field("text"),
            question_category = helpers.create_field("list"),
            exam_category = helpers.create_field("text"),
            exam_temp_name1= helpers.create_field("text"),
            question_list=helpers.create_field("list",False,dict(
                ques_category=helpers.create_field("text"),
            )),
            retake_exam = helpers.create_field("object"),
            retake_all = helpers.create_field("text"),
            retake_condition = helpers.create_field("text"),
            result_less = helpers.create_field("text"),
            retake_time = helpers.create_field("bool"),
            list_time_retake=helpers.create_field("list"),
            range_time =helpers.create_field("object"),
            scoring_method= helpers.create_field("text"),
            show_result= helpers.create_field("text"),
            customize= helpers.create_field("text"),
            minium_score= helpers.create_field("text"),
            add_feedback= helpers.create_field("text"),
            result_type= helpers.create_field("text"),
            assign_exam= helpers.create_field("text"),
            minimum_score= helpers.create_field("numberic"),
            certificate= helpers.create_field("text"),
            display_result= helpers.create_field("text"),
            ques_order= helpers.create_field("text"),
            ques_navi = helpers.create_field("bool"),
            allow_candidates = helpers.create_field("bool"),
            preview_time= helpers.create_field("bool"),
            text_high  = helpers.create_field("bool"),
            ques_dis = helpers.create_field("bool"),
            result_SMS = helpers.create_field("bool"),
            result_email = helpers.create_field("bool"),
            pause_resume = helpers.create_field("bool"),
            check_plagi = helpers.create_field("bool"),
            show_hint = helpers.create_field("bool"),
            duration=helpers.create_field("text"),
            edit_instruction=helpers.create_field("text")

        )
        _hasCreated=True
    ret = db_context.collection("LMSLS_ExExamination")

    return ret