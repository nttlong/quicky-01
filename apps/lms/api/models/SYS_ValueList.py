from config import database, helpers, db_context
import base
helpers.extent_model(
            "SYS_ValueList",
            "base",
            [["language", "list_name"]],
            language=helpers.create_field("text"),
            list_name=helpers.create_field("text"),
            values=helpers.create_field("list",False,dict(
                value = helpers.create_field("numeric"),
                caption = helpers.create_field("text"),
                custom = helpers.create_field("text")
                )),
            multi_select=helpers.create_field("bool"),
            description=helpers.create_field("text"),
            created_on=helpers.create_field("date"),
            created_by=helpers.create_field("text"),
            modified_on=helpers.create_field("date"),
            modified_by=helpers.create_field("text")
        )
def SYS_ValueList():
    ret = db_context.collection("SYS_ValueList")

    return ret