# -*- coding: utf-8 -*-
from quicky import applications
from qmongo import helpers, database
from . import base
from .. import  settings
model_name="provinces"
helpers.extent_model(
            model_name,
            "base_category",
            []
        )
def provinces():
    ret = settings.db().collection(model_name)
    return ret