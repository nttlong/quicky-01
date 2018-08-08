# -*- coding: utf-8 -*-
from quicky import applications
from qmongo import helpers,database
_hasCreated=False
from quicky import applications
app=applications.get_app_by_file(__file__)
_model_name="views"
def view():
    global _hasCreated
    if not _hasCreated:
        helpers.define_model(
            _model_name,
            [["View","App"]],
            View=helpers.create_field("text", True),
            App=helpers.create_field("text", True),
            CreatedOn=helpers.create_field("date",True),
            CreatedBy=helpers.create_field("text",True),
            Description=helpers.create_field("text",True)
        )
        _hasCreated=True
    ret = app.settings.DB.collection(_model_name)
    return ret