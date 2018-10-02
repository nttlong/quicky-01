from .. import models


def check_exits_courseCode_within_courseGroup(list_course_group):
    list_courseCode = models.HCSLS_TrainCourseGroup().aggregate().match("train_group_code in {0}", list_course_group).get_list()
    if (list_courseCode != None) and len(list_courseCode) > 0:
        return True
    return False


def get_train_course_group():
    ret=models.HCSLS_TrainCourseGroup().aggregate()
    ret.left_join(models.HCSLS_TrainCourseGroup(), "parent_code", "train_group_code", "fa")
    ret.left_join(models.models_per.auth_user_info(), "created_by", "username", "uc")
    ret.left_join(models.models_per.auth_user_info(), "modified_by", "username", "um")
    ret.project(
        _id = "_id",
        train_group_code = "train_group_code",
        train_group_name = "train_group_name",
        train_group_name2 = "train_group_name2",
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
        display_parent_code="fa.train_group_name"
        )
    ret.sort(dict(
        ordinal = 1
    )) 
    return ret




