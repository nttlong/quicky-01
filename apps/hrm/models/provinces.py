# -*- coding: utf-8 -*-
from quicky import applications
from qmongo import helpers, database
from . import base

_hasCreated = False
model_name="provinces"
def provinces():
    global _hasCreated
    if not _hasCreated:
        helpers.extent_model(
            model_name,
            "base_category",
            []
        )
        _hasCreated = True
    ret = applications.get_settings().database.collection(model_name)
    # ret.turn_never_use_schema_on()

    return ret