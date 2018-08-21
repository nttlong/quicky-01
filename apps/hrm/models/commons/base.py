from quicky import applications
from qmongo import helpers,database
from qmongo import define,extends
import datetime
import threading
model_name = "base_category"
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
    if data.get('is_delete',None) == None:
        data.update({
            'is_delete':False
        })
    if data.hashkey('name'):
        if data['name'].hashkey('default'):
            if not data['name'].hashkey('foreign'):
                data['name'].update({'foreign':data['name']['default']})
            if not data['name'].hashkey('native'):
                data['name'].update({'native':data['name']['default']})


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

base_model_info =dict(
    code = ("text",True),
    name=("object",True,
          dict(native=("text",False),
               foreign =("text",False),
               default =("text",True)
               )
          ),
    description="text",
    created_on=("date", True),
    created_on_utc=("date", True),
    created_by=("text", True),
    modified_on=("date", False),
    modified_on_utc=("date", False),
    modified_by=("text", False),
    is_delete =("bool",True),
    ordinal = ("number",False)
)
define(
    model_name,
    [["code"]],
    base_model_info
)
helpers.events("base_category")\
    .on_before_insert(on_before_insert)\
    .on_before_update(on_before_update)