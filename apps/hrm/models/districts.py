# -*- coding: utf-8 -*-
from quicky import applications
from qmongo import helpers, database
from . commons import base
from .. import settings
model_name="districts"
helpers.extent_model(
            model_name,
            "base_category",
            [],
            _provinces_id=("object")
        )
def districts():
    ret = settings.db().collection(model_name)
    return ret