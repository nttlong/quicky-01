# -*- coding: utf-8 -*-
from quicky import applications
from qmongo import helpers, database
from . import base_employee

_hasCreated = False
model_name="employees"
def employees():
    global _hasCreated
    if not _hasCreated:
        helpers.extent_model(
            model_name,
            "base_employee",
            [],
            first_name = helpers.create_field("text",True),
            last_name =helpers.create_field("text",True),
            department_id =helpers.create_field("object",True),
            position_id =helpers.create_field("object",True)
        )
        _hasCreated = True
    ret = applications.get_settings().database.collection(model_name)
    # ret.turn_never_use_schema_on()

    return ret