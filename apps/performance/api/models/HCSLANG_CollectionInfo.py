from config import database, helpers, db_context
import datetime
helpers.extent_model(
            "HCSLANG_CollectionInfo",
            "base",
            [],
            language = ("text",True),
            field_path=("text",True),
            default_caption=("text",True),
            custom_caption=("text"),

            created_on=("date"),
            created_by=("text"),
            modified_on=("date"),
            modified_by=("text")
        )
def HCSLANG_CollectionInfo():
    ret = db_context.collection("HCSLANG_CollectionInfo")
    return ret

