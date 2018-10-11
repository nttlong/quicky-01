# -*- coding: utf-8 -*-
from quicky import applications
from qmongo import helpers, database,define,extends
from . import base
model_name="base_org"
extends(
    model_name,
    "base_category",
    [],
    dict(
        parent_id=("object"),
        path_code=("list")
        )
    )