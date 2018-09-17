from qmongo import define
model_name ="schemas"
define(
    model_name,
    [["schema"]],
    schema = ("text",True),
    description = ("text")
)