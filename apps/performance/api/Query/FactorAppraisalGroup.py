from .. import models
import qmongo

def check_exits_factCode_within_factGroup(list_factor_group):
    list_factCode = qmongo.models.TMLS_FactorAppraisal.aggregate.match("factor_group_code in {0}", list_factor_group).get_list()
    if (list_factCode != None) and len(list_factCode) > 0:
        return True
    return False


def get_factor_appraisal_group():
    ret=qmongo.models.TMLS_FactorAppraisalGroup.aggregate
    ret.left_join(qmongo.models.auth_user_info, "created_by", "username", "uc")
    ret.left_join(qmongo.models.auth_user_info, "modified_by", "username", "um")
    ret.project(
        _id = "_id",
        factor_group_code = "factor_group_code",
        factor_group_name = "factor_group_name",
        factor_group_name2 = "factor_group_name2",
        parent_code = "parent_code",
        level = "level",
        level_code = "level_code",
        ordinal = "ordinal",
        note = "note",
        lock = "lock",
        created_by="uc.login_account",
        created_on= "created_on",
        modified_on="switch(case(modified_on!='',modified_on),'')",
        modified_by="switch(case(modified_by!='',um.login_account),'')",
        )
    ret.sort(dict(
        ordinal = 1
    )) 
    return ret




