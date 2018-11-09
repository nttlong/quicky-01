from qmongo import qview
from ..models.SYS_ValueList import SYS_ValueList

def SYS_VW_ValueList():
    return qview.create_mongodb_view(
        SYS_ValueList().aggregate().unwind("values").project(
            language = "language",
            list_name = "list_name",
            multi_select = "multi_select",
            description = "description",
            created_on = "created_on",
            created_by = "created_by",
            modified_on = "modified_on",
            modified_by = "modified_by",
            value = "values.value",
            caption = "values.caption",
            custom = "values.custom"
            )
        ,
        "SYS_VW_ValueList"
        )