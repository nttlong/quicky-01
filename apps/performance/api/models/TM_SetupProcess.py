from config import database, helpers, db_context
_hasCreated = False
def TM_SetupProcess():
    global _hasCreated
    if not _hasCreated:
        helpers.extent_model(
            "TM_SetupProcess",
            "base",
            [["process_id"]],
            process_id=helpers.create_field("text", True),
            process_name=helpers.create_field("text", True),
            function_id=helpers.create_field("text"),
            is_not_apply_process=helpers.create_field("bool"),
            max_approve_level=helpers.create_field("numeric"),
            is_approve_by_dept=helpers.create_field("bool"),
            is_require_reason=helpers.create_field("bool"),
            is_require_when_approve=helpers.create_field("bool"),
            is_require_when_reject=helpers.create_field("bool"),
            is_show_list_approver=helpers.create_field("bool"),
            is_reselect_approver=helpers.create_field("bool"),
            is_require_attach_file=helpers.create_field("bool"),
            file_size_limit=helpers.create_field("numeric"),
            exclude_file_types=helpers.create_field("text"),
            is_email_cancel=helpers.create_field("bool"),
            is_email_delete=helpers.create_field("bool"),
            is_email_instead=helpers.create_field("bool"),
            email_send_code=helpers.create_field("text"),
            email_send_to=helpers.create_field("list"),
            email_send_cc=helpers.create_field("list"),
            email_send_more=helpers.create_field("text"),
            email_cancel_code=helpers.create_field("text"),
            email_cancel_to=helpers.create_field("list"),
            email_cancel_cc=helpers.create_field("list"),
            email_cancel_more=helpers.create_field("text"),
            email_delete_code=helpers.create_field("text"),
            email_delete_to=helpers.create_field("list"),
            email_delete_cc=helpers.create_field("list"),
            email_delete_more=helpers.create_field("text"),
            email_instead_code=helpers.create_field("text"),
            email_instead_to=helpers.create_field("list"),
            email_instead_cc=helpers.create_field("list"),
            email_instead_more=helpers.create_field("text"),
            is_send_email_pronto=helpers.create_field("bool"),
            is_send_email_once=helpers.create_field("bool"),
            send_email_once_from_hour=helpers.create_field("text"),
            send_email_once_to_hour=helpers.create_field("text"),
            process_level_apply_for=helpers.create_field("numeric"),
            score_by=helpers.create_field("numeric"),
            score_by_coeff=helpers.create_field("list")
        )
        _hasCreated = True
    ret = db_context.collection("TM_SetupProcess")

    return ret
