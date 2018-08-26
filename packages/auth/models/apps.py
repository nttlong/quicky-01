from qmongo import define
model_name ="apps"
define(
    model_name,
    [["name"],
     ["name","schemas"],
     ["name","views.path"]],
    name = ("name",True),
    schemas=("list",True,"text"),
    views = ("list",False,dict(
        path = ("text",True),
        name = ("text",False),
        description=("text",False),
        is_public =("bool",True),
        privileges =("list",True,"text"),
        roles=("list",False,dict(
            role=("text",True),
            privileges=("list",True,"text"),
            is_full_access = ("bool",True)
        ))
    ))
)