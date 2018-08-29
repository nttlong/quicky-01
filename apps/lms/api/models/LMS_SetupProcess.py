from config import database, helpers, db_context
_hasCreated=False
def LMS_SetupProcess():
    global _hasCreated
    if not _hasCreated:
        helpers.define_model(
            "LMS_SetupProcess",
            [["process_id"]],
            process_id=helpers.create_field("int", True),
            process_name=helpers.create_field("text", True),
            function_id=helpers.create_field("text"),
            is_not_apply_process=helpers.create_field("bool"),
            max_approve_level=helpers.create_field("int"),
            is_select_approver=helpers.create_field("bool"),
            is_approve_by_dept=helpers.create_field("bool"),
            is_require_reason=helpers.create_field("bool"),
            is_require_when_approve=helpers.create_field("bool"),
            is_require_when_reject=helpers.create_field("bool"),
            sender_value=helpers.create_field("text"),
            file_size_limit=helpers.create_field("numberic"),
            exclude_file_types=helpers.create_field("text"),
            email_send_code=helpers.create_field("text"),
            email_send_to=helpers.create_field("text"),
            email_send_cc=helpers.create_field("text"),
            is_send_email_pronto=helpers.create_field("bool"),
            is_send_email_once=helpers.create_field("bool"),
            is_send_email_once_from_hour=helpers.create_field("text"),
            is_send_email_once_to_hour=helpers.create_field("text"),
            created_on=helpers.create_field("date"),
            created_by=helpers.create_field("text"),
            modified_on=helpers.create_field("date"),
            modified_by=helpers.create_field("text"),
        )
        _hasCreated=True
    ret = db_context.collection("LMS_SetupProcess")

    return ret