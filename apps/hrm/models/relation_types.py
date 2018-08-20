from qmongo import extends
from . commons import base
model_name="relation_types"
extends(
    model_name,
    base.model_name,
    [],
    is_family_cir_deduction=("bool",True)
)