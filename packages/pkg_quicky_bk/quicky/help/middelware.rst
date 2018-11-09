Multi tenancy
--------------
In  MIDDLEWARE_CLASSES of django app settings, at settings.py or json config file in configs add item:

    .. code-block::

        MIDDLEWARE_CLASSES:[
            "quicky.middleware.extension"
        ]


