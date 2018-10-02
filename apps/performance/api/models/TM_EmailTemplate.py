from config import database, helpers, db_context
import base
from .. import common
helpers.extent_model(
            "TM_EmailTemplate",
            "base",
            [["email_template_code"]],
            rec_id=("text", True),
            email_template_code=("text", True),
            email_template_name=("text", True),
            description=("text"),
            subject=("text", True),
            body=("text"),
            module_name=("text", True)
)

def on_before_insert(data):
    data.update(rec_id = common.generate_guid())

def on_before_update(data):
    pass

helpers.events("TM_EmailTemplate").on_before_insert(on_before_insert).on_before_update(on_before_update)

def TM_EmailTemplate():
    ret = db_context.collection("TM_EmailTemplate")
    return ret