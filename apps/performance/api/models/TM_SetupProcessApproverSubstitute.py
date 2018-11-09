from config import database, helpers, db_context
helpers.extent_model(
            "TM_SetupProcessApproverSubstitute",
            "base",
            [['process_id', 'process_code', 'substitute_code']],
            process_id=helpers.create_field("int", True),
            process_code=helpers.create_field("text", True),
            substitute_code=helpers.create_field("text"),
            from_date=helpers.create_field("date"),
            to_date=helpers.create_field("date"),
            note=helpers.create_field("text"),
            created_on=helpers.create_field("date"),
            created_by=helpers.create_field("text"),
            modified_on=helpers.create_field("date"),
            modified_by=helpers.create_field("text"),
        )
def TM_SetupProcessApproverSubstitute():
    ret = db_context.collection("TM_SetupProcessApproverSubstitute")

    return ret
