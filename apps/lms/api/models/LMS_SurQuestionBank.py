from config import database, helpers, db_context
import base
helpers.extent_model(
            "LMS_SurQuestionBank",
            "base",
            [["category_id", "category_name", "category_group"]],
            question_id=("text", True),
            category_name=("text", True),
            category_name2=("text"),
            category_group=("numeric"),
            ordinal=("bool"),
            active=("text"),
            level=helpers.create_field("numeric"),
            level_code=helpers.create_field("list"),
            created_on=("date"),
            created_by=("text"),
            modified_on=("date"),
            modified_by=("text")
        )
def LMS_SurQuestionBank():
    ret = db_context.collection("LMS_SurQuestionBank")
    return ret