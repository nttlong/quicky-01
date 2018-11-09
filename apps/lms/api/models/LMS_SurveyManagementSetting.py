from config import database, helpers, db_context
import base
helpers.extent_model(
            "LMS_SurveyManagementSetting",
            "base",
            [["survey_id"]],
             ques_order=("text"),
            allow_pause_resumse=("bool"),
            allow_anony_survey=("bool"),
            prevent_num_res=("bool"),
            ques_nav_sur=("bool"),
            survey_time_limit=("text"),
            survey_res_limit=("text"),
            show_process_bar=("bool"),
            show_ques_num=("bool"),
            allow_res_edit=("bool"),
            notif_email_temp=("text"),
            notif_send_to=("text"),
            notif_CC=("text"),
            notif_BCC=("text"),
            notif_send_mail=("numeric"),
            notif_from_date=("date"),
            notif_to_date=("date"),
            notif_from_time=("date"),
            notif_to_time=("date"),
            survey_send_email_again=("text"),
            confirm_email_temp=("text"),
            confirm_send_to=("text"),
            confirm_CC=("text"),
            confirm_BCC=("text"),
            confirm_send_mail=("numeric"),
            confirm_from_date=("date"),
            confirm_to_date=("date"),
            confirm_from_time=("date"),
            confirm_to_time=("date"),
            course_evalua_students=("bool"),
            survey_temp_students=("text"),
            course_evalua_teachers=("bool"),
            survey_temp_teachers=("text"),
            course_evalua_dept=("bool"),
            survey_temp_dept=("text"),
            supplier_evalua_dept=("bool"),
            survey_temp_sup_dept=("text"),
            emp_voice=("bool"),
            survey_temp_emp_voice=("text"),
            other_sur=("bool"),
            survey_temp_other=("text"),


           
        )
def LMS_SurveyManagementSetting():
    ret = db_context.collection("LMS_SurveyManagementSetting")
    return ret