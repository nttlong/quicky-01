from config import database, helpers, db_context
import base
_hasCreated=False
def HCSSYS_FunctionListSummary():
    global _hasCreated
    if not _hasCreated:
        helpers.extent_model(
            "HCSSYS_FunctionListSummary",
            "base",
            [["function_id"]],
            function_id=helpers.create_field("text", True),
            query=helpers.create_field("text", True),
            collection=helpers.create_field("numeric"),
            created_on=helpers.create_field("text"),
            created_by=helpers.create_field("date"),
            modified_on=helpers.create_field("text"),
            modified_by=helpers.create_field("date")
        )
        _hasCreated=True
    ret = db_context.collection("HCSSYS_FunctionListSummary")

    return ret