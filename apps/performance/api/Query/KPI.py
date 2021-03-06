from .. import models
import qmongo
from .. import common
def display_list_kpi(group_code):
    ret=qmongo.models.TMLS_KPI.aggregate
    ret.join(qmongo.models.TMLS_KPIGroup, "kpi_group_code", "kpi_group_code", "fag")
    ret.left_join(qmongo.models.auth_user_info, "created_by", "username", "uc")
    ret.left_join(qmongo.models.auth_user_info, "modified_by", "username", "um")
    if group_code != None and group_code != "":
        ret.match('fag.level_code == {0}', group_code)
    ret.project(
        kpi_code = "kpi_code",
        kpi_name = "kpi_name",
        kpi_name2 = "kpi_name2",
        kpi_group_code = "kpi_group_code",
        unit_code = "unit_code",
        cycle_type="cycle_type",
        kpi_desc="kpi_desc",
        kpi_ref="kpi_ref",
        weight="weight",
        benchmark="benchmark",
        score_from="score_from",
        score_to="score_to",
        kpi_formula="kpi_formula",
        value_cal_type="value_cal_type",
        input_type="input_type",
        is_apply_all="is_apply_all",
        kpi_years="kpi_years",
        note="note",
        lock="lock",
        created_by="uc.login_account",
        created_on="created_on",
        modified_on="switch(case(modified_on!='',modified_on),'')",
        modified_by="switch(case(modified_by!='',um.login_account),'')",
        )
    ret.sort(dict(
        kpi_code = 1
        ))

    return ret
