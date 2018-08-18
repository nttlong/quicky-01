# -*- coding: utf-8 -*-
from quicky import applications
from qmongo import helpers, database
from . import base_employee
from .. import settings
import qmongo
model_name="employees"
qmongo.extends(
    model_name,
    "base_employee",
    [],
    first_name =("text",True),
    last_name =("text",True),
    gender = ("bool",True),
    birthdate = ("date",False),
    department_id =("object",True),
    position_id =("object",True)
    )
def employees():
    ret = settings.db().collection(model_name)
    return ret