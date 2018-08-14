import quicky
import hrm.forms as forms
from qmongo import helpers
from qmongo import database
from quicky import encryptor
import threading
from bson import *
from .. import settings
app=quicky.applications.get_app_by_file(__file__)
db=database.connect(app.settings.Database)

__cache_models={}
def get_coll(source_id):
    import os
    import importlib
    source_name = encryptor.get_value(source_id)
    dir = os.path.dirname(app.mdl.__file__)
    model_path = dir + os.sep +"models"+ os.sep + source_name + ".py"
    if not os.path.isfile(model_path):
        dir = os.path.dirname(app.mdl.__file__)
        dir = dir + os.sep + "models"
        tem_file = dir + os.sep + "model.txt"
        file = open(tem_file, "r")
        txt = file.read()
        file.close()
        txt_content = txt.replace("@model_name", source_name)
        file_code=open(model_path, "w")
        file_code.write(txt_content)
        file_code.close()

    coll = importlib.import_module(app.mdl.__name__ + ".models." + source_name)
    return getattr(coll,source_name)

def get_list(params):
    coll = get_coll(params["data"]["source"])
    qr = coll().aggregate()
    if params["data"].get("params",None) != None:
        for x in params["data"]["params"].get("sort",[]):
            qr=qr.sort({
                x["colId"]:(lambda p: 1 if p["sort"]=="asc" else -1)(x)
            })
        if params["data"]["params"].get("filter") != {}:
            for x in params["data"]["params"]["filter"].keys():
                f= params["data"]["params"]["filter"][x]
                if f["type"] == "contains":
                    expr="contains("+x+",{0})"
                    qr=qr.match(expr,f["filter"])
                if f["type"] == "notEqual":
                    expr=x+"!={0}"
                    qr=qr.match(expr,f["filter"])
                if f["type"] == "equals":
                    expr=x+"=={0}"
                    qr=qr.match(expr,f["filter"])
                if f["type"] == "notEqual":
                    expr=x+"!={0}"
                    qr=qr.match(expr,f["filter"])
                if f["type"] == "startsWith":
                    expr = "start(" + x + ",{0})"
                    qr = qr.match(expr, f["filter"])
                if f["type"] == "endsWith":
                    expr = "end(" + x + ",{0})"
                    qr = qr.match(expr, f["filter"])
                if f["type"] == "notContains":
                    expr = "notContains(" + x + ",{0})"
                    qr = qr.match(expr, f["filter"])





    data =qr.get_page(params["data"].get("pageIndex",0),params["data"].get("pageSize",50))
    return data
def update_item(args):
    coll = get_coll(args["data"]["source"])
    ret= coll().update(args["data"]["item"],"code == {0}",args["data"]["item"]["code"])
    return ret["error"]
def add_new_item(args):
    coll = get_coll(args["data"]["source"])
    ret = coll().insert(args["data"]["item"])

    return ret["error"]
def get_item(params):
    coll= get_coll(params["data"]["source"])
    item=coll().aggregate().match("code=={0}",params["data"]["code"]).get_item();

    return item
def save_item(params):
    category_name = params["view"].split('/')[params["view"].split('/').__len__()-1]
    frm = getattr(forms, category_name)
    coll_name = frm.layout.get_config()["collection"]
    data = params["data"]
    coll = db.collection(coll_name)
    ret=None
    if data.get("_id",None)==None:
        ret=coll.insert(data)
    else:
        update_fields=frm.layout.get_all_fields_of_form()
        update_data={}
        for key in update_fields:
            if data.has_key(key) and key not in frm.layout.get_config().get("keys",[]):
                update_data.update({
                    key:data[key]
                })
        ret=coll.update(update_data,"_id==@id",id=ObjectId(data["_id"]))
        if ret.get("error",None)!=None:
            ret=dict(
                error=ret["error"],
                data=data
            )
        else:
            ret = dict(
                data=data
            )

    return ret
def get_dictionary(params):
    category_name = params["view"].split('/')[1]
    frm = getattr(forms, category_name)
    data =params["data"]
    source_id=params["data"]["source"]
    source=hash_data.from_hash(source_id)

    frm = getattr(forms, category_name)
    lookup=frm.layout.get_lookup_config_by_source(source)
    ret_data=db.collection(lookup["source"]).aggregate().project(
        _id="0",
        value=lookup["lookup_field"],
        text=lookup["display_field"]
    ).get_list()
    return ret_data



