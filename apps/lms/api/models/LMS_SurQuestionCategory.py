from config import database, helpers, db_context
import base
helpers.extent_model(
            "LMS_SurQuestionCategory",
            "base",
            [["category_id", "category_name", "category_group"]],
            category_id=("text", True),
            category_name=("text", True),
            category_name2=("text"),
            category_group=("numeric"),
            ordinal=("numeric"),
            note=("text"),
            active=("bool"),
            created_on=("date"),
            created_by=("text"),
            modified_on=("date"),
            modified_by=("text")
        )
def LMS_SurQuestionCategory():
    ret = db_context.collection("LMS_SurQuestionCategory")
    return ret