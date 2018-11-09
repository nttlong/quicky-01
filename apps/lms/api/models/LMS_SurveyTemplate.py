from config import database, helpers, db_context
import base
helpers.extent_model(
            "LMS_SurveyTemplate",
            "base",
            [["survey_id"]],
            survey_id=("text", True),
            survey_type=("numeric", True),
            temp_survey_1=("text", True),
            temp_survey_2=("text"),
            order=("numeric"),
            active=("bool"),
            question_list=("list"),
            created_on=("date"),
            created_by=("text"),
            modified_on=("date"),
            modified_by=("text"),
        )
def LMS_SurveyTemplate():
    ret = db_context.collection("LMS_SurveyTemplate")
    return ret