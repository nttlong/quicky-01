from qmongo import define
model_name = "roles"
define(
    model_name,
    [["role"],
     ["name"],
     ["role","schemas.name"]],
    role=("text",True),
    name=("text",True),
    description=("text"),
    apps=("list",False,dict(
        name=("text",True),
        is_full_access=("bool",True),
        schemas=("list",True,dict(
            name=("text",True),
            is_full_access=("bool",True)
        )),
        views=("list",False,dict(
            name=("text",True),
            privileges=("object",False,dict(
                    is_allow_view=("bool",True),
                    is_allow_insert = ("bool",True),
                    is_allow_update = ("bool",True),
                    is_allow_import = ("bool",True),
                    is_allow_export = ("bool",True),
                    features = ("list",False,dict(
                        name=("text",True)
                    ))

            )),
            users=("list",False,dict(
                    username=("text",True),
                    is_allow_view=("bool",True),
                    is_allow_insert = ("bool",True),
                    is_allow_update = ("bool",True),
                    is_allow_import = ("bool",True),
                    is_allow_export = ("bool",True),
                    features = ("list",False,dict(
                        name=("text",True)
                    ))
                ))
            )
        ))
    )
)
