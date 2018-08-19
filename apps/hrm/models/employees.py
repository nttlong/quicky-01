# -*- coding: utf-8 -*-
from quicky import applications
from qmongo import helpers, database
from . commons import base_employee
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
    _departments_id =("object",False),
    _positions_id =("object",False),
    _job_works_id=("object"),
    legal_info=(
        "object",
        False,
        dict(
            id_card=("text",True),
            issue_date=("date",True),
            _provinces_id=("object",True),
            description = ("text")
        )
    ),
    salary_info = (
        "list",
        False,
        dict(
            _salary_info_id=("object",True),
            is_active = ("bool",True),
            apply_date = ("date",True),
            decision_no = ("text",False),
            decision_date = ("date",True),
            description ="text"
        )
    )
)
def employees():
    ret = settings.db().collection(model_name)
    return ret