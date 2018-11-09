from config import database, helpers, db_context
helpers.define_model(
            "SYS_FunctionList_Favorite",
            [["function_id"]],
            sorting=("text"),
            description=("text"),
            custom_name=("text"),
            style_class=("text"),
            url=("text"),
            image=("text"),
            default_name=("text", True),
            height=("text"),
            parent_id=("text"),
            active=("bool"),
            function_id=("text", True),
            type=("text"),
            width=float,
            icon=str,
            app=str,
            level_code=list,
            color=object,
        )
def SYS_FunctionList_Favorite():
    ret = db_context.collection("SYS_FunctionList_Favorite")
    return ret