from config import database, helpers, db_context
import datetime
helpers.extent_model(
            "HCSSYS_ComboboxList",
            "base",
            [["combobox_code", "language"]],
            combobox_code = ("text",True),
            language=("text", True),
            display_name=("text"),
            description=("text"),
            table_name=("text"),
            table_fields=("list"),
            display_fields=("list"),
            predicate=("list", False, dict(
                column = ("string"),
                operator = ("string")
                )),
            value_field=("text"),
            caption_field=("text"),
            sorting_field=("object"),
            filter_field=("text"),
            multi_select=("bool"),
            parent_field=("text"),
            page_size=("int"),
            created_on=("date"),
            created_by=("text"),
            modified_on=("date"),
            modified_by=("text"),
        )
def HCSSYS_ComboboxList():
    ret = db_context.collection("HCSSYS_ComboboxList")
    return ret