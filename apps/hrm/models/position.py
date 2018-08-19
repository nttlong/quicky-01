# -*- coding: utf-8 -*-
from quicky import applications
from qmongo import helpers, database
from . commons import base
from .. import settings
from qmongo import extends,extends_dict,define
model_name="position"
extends(
    model_name,
    "base_category",
    [],
    details=("list",False,
             extends_dict(base.base_model_info,
                          seniority_from =("number",True),
                          seniority_to =("number",True),
                          coefficient = ("numeric",True),
                          salary = ("numeric",True)
                          ),
             )
)
def position():
    ret = settings.db().collection(model_name)
    return ret