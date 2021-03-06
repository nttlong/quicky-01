from .. import models
import qmongo
def display_list_apr_period(search_text):
    ret=qmongo.models.TMPER_AprPeriod.aggregate
    ret.left_join(qmongo.models.auth_user_info, "created_by", "username", "uc")
    ret.left_join(qmongo.models.auth_user_info, "modified_by", "username", "um")
    ret.project(
        apr_period="apr_period",
        apr_year="apr_year",
        emp_final_from="emp_final_from",
		emp_final_to="emp_final_to",
        approval_final_from="approval_final_from",
        approval_final_to="approval_final_to",
        give_target_from="give_target_from",
        give_target_to="give_target_to",
        review_mid_from="review_mid_from",
        review_mid_to="review_mid_to",
		approval_mid_from="approval_mid_from",
        approval_mid_to="approval_mid_to",
        created_by="uc.login_account",
        created_on="created_on",
        modified_on="switch(case(modified_on!='',modified_on),'')",
        modified_by="switch(case(modified_by!='',um.login_account),'')",
        )
    if(search_text!= None and search_text != ''):
        ret.match("contains(apr_year,@name)"
                  + "or contains(apr_period,@name)",name=search_text.strip())
    ret.sort(dict(
        apr_year = -1, apr_period = -1
        ))

    return ret

