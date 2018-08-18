# -*- coding: utf-8 -*-
from quicky import applications
from qmongo import helpers, database
from . import base
from . import base_org
from .. import settings
model_name="departments"
helpers.extent_model(
        model_name,
        "base_org",
        [],
        contact=("object",
                 False,
                 dict(
                     tel="text",
                     fax="text",
                     email="text",
                     address="text"
                     )
                 ),
        test  =("text",True)

    )
def departments():
    ret = settings.db().collection(model_name)
    return ret