from config import database, helpers, db_context
import base
from .. import common
helpers.extent_model(
            "HCSSYS_AttachmentFile",
            "base",
            [["email_template_code"]],
            rec_id = ("text", True),
            function_id=("text", True),
            file_name=("text", True),
            file_type=("text", True),
            attachment=("text"),
            file_size=("numeric"),
            category=("text"),
            location=("text"),
            table_name=("text", True),
            field_name=("text", True),
            field_value=("text", True),
            description=("text"),
            access_type=("numeric", True),
            computer_name=("text")
)

def on_before_insert(data):
    data.update(rec_id = common.generate_guid())

def on_before_update(data):
    pass

helpers.events("HCSSYS_AttachmentFile").on_before_insert(on_before_insert).on_before_update(on_before_update)

def HCSSYS_AttachmentFile():
    ret = db_context.collection("HCSSYS_AttachmentFile")
    return ret