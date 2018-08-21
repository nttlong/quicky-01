from qmongo import extends, extends_dict
from . commons import base
model_name = "employee_types"
extends(
    model_name,
    base.model_name,
    [],
    formular = ("text")
)

