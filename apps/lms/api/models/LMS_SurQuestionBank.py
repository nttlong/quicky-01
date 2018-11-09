from config import database, helpers, db_context
import base
helpers.extent_model(
            "LMS_SurQuestionBank",
            "base",
            [["question_id"]],
            question_id=("text", True),
            category_id=("text", True),
            category_type=("numeric", True),
            question_content_1=("text"),
            question_content_2=("text"),
            question_description=("text"),
            ordinal=("numeric"),
            active=("bool"),
            level=helpers.create_field("numeric"),
            level_code=helpers.create_field("list"),
            created_on=("date"),
            created_by=("text"),
            modified_on=("date"),
            modified_by=("text"),
            question_options=("list"),
            question_other_field=("bool"),
            question_random_options=("bool"),
            question_require_answer=("bool"),
            question_note=("text"),
        )
def LMS_SurQuestionBank():
    ret = db_context.collection("LMS_SurQuestionBank")
    return ret