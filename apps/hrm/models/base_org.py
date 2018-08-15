# -*- coding: utf-8 -*-
from quicky import applications
from qmongo import helpers, database
from . import base
from .. import settings
_hasCreated = False
model_name="base_org"
global _hasCreated
if not _hasCreated:
    helpers.extent_model(
        model_name,
        "base_category",
        [],
        dict(
            parent_id=helpers.create_field("object"),
            path_code=helpers.create_field("list")
        )

    )
    _hasCreated = True
ret = settings.db().collection(model_name)