from config import database, helpers, db_context
import datetime
helpers.extent_model(
            "HCSSYS_CollectionInfo",
            "base",
            [],
            table_name = ("text",True),
            field_name=("text",True),
            data_type=("text",True),
            data_length=("numeric"),
            default_value=("text"),
            is_unique=("bool"),
            description=("text"),
            is_parent=("bool"),
            parent_field=("text"),
            field_path=("text", True),
            created_on=("date"),
            created_by=("text"),
            modified_on=("date"),
            modified_by=("text")
        )
def HCSSYS_CollectionInfo():
    ret = db_context.collection("HCSSYS_CollectionInfo")
    return ret
