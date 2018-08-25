from qmongo import define
model_name="apps"
define(
    model_name,
    [["code"]],
    code = ("text",True),
    name = ("object",True,dict(
        default=("text",True),
        foreign = ("text",False)
    )),
    description=("text",False),
    support_schemas=("list",True,"text")

)