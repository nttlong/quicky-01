# -*- coding: utf-8 -*-
from quicky import applications
from qmongo import helpers, database
from . import base
from .. import settings
model_name="districts"
helpers.extent_model(
            model_name,
            "base_category",
            []
        )
def districts():
    ret = settings.db().collection(model_name)
    return ret