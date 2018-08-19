# -*- coding: utf-8 -*-
from quicky import applications
from qmongo import helpers, database
from . commons import base
from . commons import base_org
from .. import settings
from qmongo import define
from qmongo import extends
model_name="departments"
extends(
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
        map_location=("object",
                      False,
                      dict(
                          latitude="number",
                          longitude = "number"
                      )),
        test  =("text",True)

    )
def departments():
    ret = settings.db().collection(model_name)
    return ret