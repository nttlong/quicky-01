from qmongo import extends,extends_dict
from . commons import base
model_name = "nations"
extends(
    model_name,
    base.model_name,
    [
        ["code","provinces.code"],
        ["code","provinces.code","provinces.districts.code"]
    ],
    description = "text",
    provinces = ("list",
                 False,
                 extends_dict(
                     base.base_model_info,
                     _province_id = ("object",True),
                     districts =("list",
                                 False,
                                 extends_dict(
                                     base.base_model_info,
                                     _district_id = ("object",True)
                                 )
                                )
                 )
                 )
)