from .. import models
import qmongo
def get_job_working_group():
    ret=qmongo.models.HCSLS_JobWorkingGroup.aggregate
    ret.left_join(qmongo.models.auth_user_info, "created_by", "username", "uc")
    ret.left_join(qmongo.models.auth_user_info, "modified_by", "username", "um")
    ret.project(
        gjw_code = 1,
        gjw_name = 1,
        gjw_name2 = 1,
        parent_code = 1,
        level = 1,
        level_code = 1,
        ordinal = 1,
        note = 1,
        lock = 1,
        created_by="uc.login_account",
        created_on="created_on",
        modified_on="switch(case(modified_on!='',modified_on),'')",
        modified_by="switch(case(modified_by!='',um.login_account),'')",
        )
    ret.sort(dict(
        ordinal = 1,
        gjw_name = 1
    ))
    return ret

