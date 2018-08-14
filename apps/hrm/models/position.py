# -*- coding: utf-8 -*-
from quicky import applications
from qmongo import helpers, database
from . import base
from .. import settings
_hasCreated = False
model_name="position"
def position():
    global _hasCreated
    if not _hasCreated:
        helpers.extent_model(
            model_name,
            "base_category",
            []
        )
        _hasCreated = True
    ret = settings.db().collection(model_name)
    # ret.turn_never_use_schema_on()

    return ret