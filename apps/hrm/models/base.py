from quicky import applications
from qmongo import helpers,database
import datetime
import threading
def on_before_insert(data):
    user = "application"
    if hasattr(threading.current_thread(),"user"):
        user = threading.current_thread().user.username
    if data.get('created_by',None)==None:
        data.update({
            "created_on":datetime.datetime.now(),
            "created_on_utc":datetime.datetime.utcnow(),
            "created_by":user
            })
def on_before_update(data):
    user = "application"
    if hasattr(threading.current_thread(),"user"):
        user = threading.current_thread().user.username
    if data.get('modified_by',None)==None:
        data.update({
            "modified_on":datetime.datetime.now(),
            "modified_on_utc":datetime.datetime.utcnow(),
            "modified_by":user
            })


helpers.define_model(
    "base_category",
    [["code"]],
    code=("text", True),
    name=("text", True),
    description="text",
    created_on=("date", True),
    created_on_utc=("date", True),
    created_by=("text", True),
    modified_on=("date", False),
    modified_on_utc=("date", False),
    modified_by=("text", False)
)
helpers.events("base_category")\
    .on_before_insert(on_before_insert)\
    .on_before_update(on_before_update)