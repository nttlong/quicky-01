from qmongo import define
model_name = "roles"
define(
    model_name,
    [["role"]],
    role = ("text",True),
    name = ("text",True),
    description = ("text",False),
    users =("list",False,"text")
)