from .. import models
from .. import common
def display_list_train_ls_course(group_code):
    ret = models.SYS_ValueList().aggregate().match("list_name == {0}", "LPeriodic")
    ret.unwind("values")
    ret.join(models.HCSLS_TrainLsCourse(),"values.value", "periodic", "fa")
    # ret = models.HCSLS_TrainLsCourse().aggregate()
    # ret.join(models.HCSLS_TrainCourseGroup(), "train_group_code", "train_group_code", "fag")
    ret.left_join(models.HCSLS_TrainCourseGroup(), "fa.train_group_code", "train_group_code", "fag")
    ret.left_join(models.models_per.auth_user_info(), "fag.created_by", "username", "uc")
    ret.left_join(models.models_per.auth_user_info(), "fag.modified_by", "username", "um")
    if group_code != None and group_code != "":
        ret.match('fag.level_code == {0}', group_code)
    ret.project(
        course_code="fa.course_code",
        course_name="fa.course_name",
        course_name2="fa.course_name2",
        course_content="fa.course_content",
        train_group_code="fa.train_group_code",
        profession_code="fa.profession_code",
        field_code="fa.field_code",
        method="fa.method",
        periodic="fa.periodic",
        number_month="fa.number_month",
        learner_min="fa.learner_min",
        learner_max="fa.learner_max",
        train_hours="fa.train_hours",
        supplier_code="fa.supplier_code",
        room_code="fa.room_code",
        activity_task="fa.activity_task",
        certificate_form="fa.certificate_form",
        after_month_work="fa.after_month_work",
        note="fa.note",
        ordinal="fa.ordinal",
        lock="fa.lock",
        created_by="uc.login_account",
        created_on="fa.created_on",
        modified_on="switch(case(fa.modified_on!='',fa.modified_on),'')",
        modified_by="switch(case(fa.modified_by!='',um.login_account),'')",
        display_periodic="switch(case(values.custom!='',values.custom),values.caption)",
        )
    ret.sort(dict(
        ordinal = 1
        ))

    return ret
