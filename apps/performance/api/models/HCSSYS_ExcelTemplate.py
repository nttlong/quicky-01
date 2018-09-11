# -*- coding: utf-8 -*-
from config import database, helpers, db_context
helpers.extent_model(
            "HCSSYS_ExcelTemplate",
            "base",
            [["function_id"], ["template_code"], ["detail.field_name", "template_code"]],
            function_id=("text", True),
            template_code=("text", True),
            template_name=("text", True),
            is_default=("bool"),
            view_name=("text", True),
            detail=("list",False,dict(
                field_name = ("text"),
                lookup_data = ("text"),
                lookup_key_field = ("text"),
                lookup_result = ("text"),
                allow_null = ("bool"),
                is_key = ("bool"),
                language = ("text"),
                header_text = ("text"),
                is_visible = ("bool"),
                ordinal = ("numeric")
                )),
            created_on=("date"),
            created_by=("text"),
            modified_on=("date"),
            modified_by=("text")
        )
def HCSSYS_ExcelTemplate():
    ret = db_context.collection("HCSSYS_ExcelTemplate")
    return ret