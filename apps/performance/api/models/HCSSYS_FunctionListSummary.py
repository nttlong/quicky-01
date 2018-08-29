from config import database, helpers, db_context
import base
helpers.extent_model(
            "HCSSYS_FunctionListSummary",
            "base",
            [["function_id"]],
            function_id=("text", True),
            query=("text", True),
            collection=("numeric"),
            created_on=("text"),
            created_by=("date"),
            modified_on=("text"),
            modified_by=("date")
        )
def HCSSYS_FunctionListSummary():
    ret = db_context.collection("HCSSYS_FunctionListSummary")
    return ret