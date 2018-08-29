# -*- coding: utf-8 -*-
from config import database, helpers, db_context
helpers.extent_model(
            "LMSLS_ExQuestionBank",
            "base",
            [["ques_id"]],
            ques_id=("text", True),
            ques_category=("text", True),
            ques_type=("numeric"),
            ques_level=("numeric"),
            ques_file=("object"),
            ques_detail_1=("text"),
            ques_detail_2=("text"),
            ques_hint=("object"),
            ques_answers=("list", False, dict(
                    text=("text"),
                    isCorrect=("bool"),
                    answers=("text"),
                    if_correct=("text"),
                    if_incorrect=("text"),
                    question=("text"),
                )),
            ques_total_marks=("object"),
            ques_attach_file=("bool"),
            ques_max_answer_time=("numeric"),
            ques_explanation=("text"),
            ques_answer_options=("numeric"),
            ques_randomization=("numeric"),
            ques_tags=("list"),
            ques_evaluated_by=("text"),
            ques_limit_on_text=("numeric"),
            ques_specify_limit=("numeric"),
        )
def LMSLS_ExQuestionBank():
    ret = db_context.collection("LMSLS_ExQuestionBank")
    return ret