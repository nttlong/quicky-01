from qmongo import define
model_name = "roles"
define(
    model_name,
    [["role","schema"]],
    role = ("text",True),
    name = ("text",True),
    schema = ("text",True),
    description = ("text",False),
    users =("list",False,"text")
)