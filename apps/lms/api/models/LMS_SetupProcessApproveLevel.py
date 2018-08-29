from config import database, helpers, db_context
from ...api import common

_hasCreated=False
def LMS_SetupProcessApproveLevel():
    global _hasCreated
    if not _hasCreated:
        helpers.define_model(
            "LMS_SetupProcessApproveLevel",
            [['rec_id']],
            rec_id =helpers.create_field("text", True),
            process_id=helpers.create_field("int", True),
            approve_level=helpers.create_field("int", True),
            approver_value=helpers.create_field("int"),
            email_approve_code=helpers.create_field("text"),
            email_approve_to=helpers.create_field("int"),
            email_approve_cc=helpers.create_field("text"),
            email_reject_code=helpers.create_field("text"),
            email_reject_to=helpers.create_field("int"),
            email_reject_cc=helpers.create_field("text"),
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

        def on_before_update(data):
            pass
        helpers.events("LMS_SetupProcessApproveLevel").on_before_insert(on_before_insert).on_before_update(on_before_update)

        _hasCreated=True
    ret = db_context.collection("LMS_SetupProcessApproveLevel")

    return ret