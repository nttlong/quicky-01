# -*- coding: utf-8 -*-
from quicky import applications
from qmongo import helpers, database
from . import base
from . import base_org
from .. import settings
_hasCreated = False
model_name="departments"
helpers.extent_model(
        model_name,
        "base_org",
        []
    )
def departments():

    ret = settings.db().collection(model_name)
    # ret.turn_never_use_schema_on()

    return ret