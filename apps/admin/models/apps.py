from qmongo import define
model_name ="apps"
define(
    model_name,
    [["name"]],
    name = ("name",True),
    schemas=("list",True,"text"),
    views = ("list",False,dict(
        path = ("text",True),
        is_public =("bool",True),
        privileges =("list",True,"text")
    ))
)