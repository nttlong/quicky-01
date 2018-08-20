# -*- coding: utf-8 -*-
from quicky import applications
from qmongo import helpers, database
from . commons import base_employee
from .. import settings
import qmongo
model_name="employees"
from qmongo import extends
extends(
    model_name,
    "base_employee",
    [[
        "contact_info.email"
    ],[
        "Dependants.id_card"
    ]],
    first_name =("text",True),
    last_name =("text",True),
    gender = ("bool",True),
    birthdate = ("date",False),
    working_info =(
        "object",
        False,
        dict(
            _departments_id =("object",False),
            _positions_id =("object",False),
            _job_works_id=("object"),
            join_date = ("date",True),

        )
    ),
    native_country=("object",
                    False,
                    dict(
                        provinces_id=("object",True),
                        _districts_id =("object",True)
                    )
    ),
    contact_info =("object",
                   False,
                   dict(
                       address="text",
                       email="text"

                   )),
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
    ),
    Dependants = ("list",
                  False,
                  dict(
                      first_name=("text",True),
                      last_name = ("text",True),
                      id_card = ("text",False),
                      issue_date=("date",False),
                      _provinces_id = ("object")
                  ))
)
# def employees():
#     ret = settings.db().collection(model_name)
#     return ret