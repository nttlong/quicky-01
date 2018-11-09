from .. import models
import qmongo
def display_list_unit():
    ret=qmongo.models.HCSLS_Unit.aggregate
    ret.left_join(qmongo.models.auth_user_info, "created_by", "username", "uc")
    ret.left_join(qmongo.models.auth_user_info, "modified_by", "username", "um")
    ret.project(
        unit_code="unit_code",
        unit_name="unit_name",
        unit_name2="unit_name2",
		note="note",
        lock="lock",
        ordinal="ordinal",
        is_default="is_default",
        data_type="data_type",
        dec_place="dec_place",
        value_list_detail="value_list_detail",
        created_by="uc.login_account",
        created_on="created_on",
        modified_on="switch(case(modified_on!='',modified_on),'')",
        modified_by="switch(case(modified_by!='',um.login_account),'')",
        )
    ret.sort(dict(
        ordinal = 1
        ))

    return ret