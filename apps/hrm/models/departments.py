# -*- coding: utf-8 -*-
from quicky import applications
from qmongo import helpers, database
from . import base
from . import base_org

_hasCreated = False
model_name="departments"
def departments():
    global _hasCreated
    if not _hasCreated:
        helpers.extent_model(
            model_name,
            "base_org",
            []
        )
        _hasCreated = True
    ret = applications.get_settings().database.collection(model_name)
    # ret.turn_never_use_schema_on()

    return ret