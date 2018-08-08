# -*- coding: utf-8 -*-
from quicky import applications
from qmongo import helpers,database
_hasCreated=False
from quicky import applications
app=applications.get_app_by_file(__file__)
def role():
    global _hasCreated
    if not _hasCreated:
        helpers.define_model(
            "roles",
            [["role","schema"],
             ["name""schema"],
             ["role","schema","apps.name"],
             ["role","schema","apps.name","apps.views.name"],
             ["role","schema","apps.name", "apps.views.name","apps.views.users.name"]
             ],
            role=helpers.create_field("text", True),
            schema=helpers.create_field("text",True),
            name=helpers.create_field("text", True),
            createdOn=helpers.create_field("date",True),
            createdBy=helpers.create_field("text",True),
            description=helpers.create_field("text",False),
            apps=helpers.create_field("list",False,detail=dict(
                name=helpers.create_field("text",True),
                views=helpers.create_field("list", False, detail=dict(
                    name=helpers.create_field("text", True),
                    users=helpers.create_field("list", False, detail=dict(
                        username=helpers.create_field("text", True),
                        createdOn=helpers.create_field("date", True),
                        createdBy=helpers.create_field("text", True),
                        description=helpers.create_field("text", False)
                    )),
                    createdOn=helpers.create_field("date", True),
                    createdBy=helpers.create_field("text", True),
                    description=helpers.create_field("text", False)
                )),
                createdOn=helpers.create_field("date", True),
                createdBy=helpers.create_field("text", True),
                description=helpers.create_field("text",False)
            ))

        )
        _hasCreated=True
    ret = app.settings.DB.collection("roles")
    return ret