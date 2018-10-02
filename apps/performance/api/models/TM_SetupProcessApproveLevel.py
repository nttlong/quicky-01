from config import database, helpers, db_context
from ...api import common
import base

_hasCreated=False
def TM_SetupProcessApproveLevel():
    global _hasCreated
    if not _hasCreated:
        helpers.define_model(
            "TM_SetupProcessApproveLevel",
            #"base",
            [['rec_id']],
            rec_id=helpers.create_field("text", True),
            process_id=helpers.create_field("int"),
            approve_level=helpers.create_field("numeric"),
            approver_value=helpers.create_field("numeric"),
            email_approve_code=helpers.create_field("text"),
            email_approve_to=helpers.create_field("list"),
            email_approve_cc=helpers.create_field("list"),
            email_approve_more=helpers.create_field("text"),
            email_reject_code=helpers.create_field("text"),
            email_reject_to=helpers.create_field("list"),
            email_reject_cc=helpers.create_field("list"),
            email_reject_more=helpers.create_field("text"),
            email_approve_cancel_code=helpers.create_field("text"),
            email_approve_cancel_to=helpers.create_field("list"),
            email_approve_cancel_cc=helpers.create_field("list"),
            email_approve_cancel_more=helpers.create_field("text"),
            email_reject_cancel_code=helpers.create_field("text"),
            email_reject_cancel_to=helpers.create_field("list"),
            email_reject_cancel_cc=helpers.create_field("list"),
            email_reject_cancel_more=helpers.create_field("text"),
            default_approver_code=helpers.create_field("text"),
            not_receive_email=helpers.create_field("bool"),
            created_on=helpers.create_field("date"),
            created_by=helpers.create_field("text"),
            modified_on=helpers.create_field("date"),
            modified_by=helpers.create_field("text"),
        )
        def on_before_insert(data):
            data.update({
                "rec_id": common.generate_guid()
                })
            # pass

        def on_before_update(data):
            pass
        helpers.events("TM_SetupProcessApproveLevel").on_before_insert(on_before_insert).on_before_update(on_before_update)

        _hasCreated=True
    ret = db_context.collection("TM_SetupProcessApproveLevel")

    return ret