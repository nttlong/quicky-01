Syntax:
-------

    from qmongo import helpers

    helpers.define_model(

        "<Model name>",

        ["{key field 1}",..,"{key field n}"],

        <field name 1 > =helpers.create_field("<text | date | bool | number | list | object >", [is require]),

        ...

        <field name n > =helpers.create_field("<text | date | bool | number | list | object >", [is require])



    )

