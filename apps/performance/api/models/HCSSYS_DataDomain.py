from config import database, helpers, db_context
import datetime
import base
import threading
helpers.extent_model(
            "HCSSYS_DataDomain",
            "base",
            [["dd_code"]],
            dd_code=("text",True),
            dd_name=("text"),
            access_mode=("numeric"),
            description=("text"),
            created_on=("date"),
            created_by=("text"),
            modified_on=("date"),
            modified_by=("text"),
            detail=("list",False,dict(
                department_code = ("text"),
                ))
        )
def on_before_insert(data):
    before_process

def on_before_update(data):
    before_process(data)

def before_process(data):
    data.update({
        "detail": [{
                "department_code":x['department_code'],
                } for x in data.get('detail',[])]
        })

helpers.events("HCSSYS_DataDomain").on_before_insert(on_before_insert).on_before_update(on_before_update)
def HCSSYS_DataDomain():
    ret = db_context.collection("HCSSYS_DataDomain")
    return ret