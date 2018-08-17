# -*- coding: utf-8 -*-
from quicky import applications
from qmongo import helpers, database
from . import base_employee
from .. import settings
model_name="employees"
helpers.extent_model(
            model_name,
            "base_employee",
            [],
            first_name = helpers.create_field("text",True),
            last_name =helpers.create_field("text",True),
            department_id =helpers.create_field("object",True),
            position_id =helpers.create_field("object",True)
        )
def employees():
    ret = settings.db().collection(model_name)
    return ret