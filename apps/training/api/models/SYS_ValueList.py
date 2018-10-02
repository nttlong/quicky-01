from config import database, helpers, db_context
helpers.define_model(
            "SYS_ValueList",
            [["language", "list_name"]],
            language=("text"),
            list_name=("text"),
            values=("list",False,dict(
                value = ("numeric"),
                caption = ("text"),
                custom = ("text")
                )),
            multi_select=("bool"),
            description=("text"),
            created_on=("date"),
            created_by=("text"),
            modified_on=("date"),
            modified_by=("text")
        )

def SYS_ValueList():
    ret = db_context.collection("SYS_ValueList")
    return ret