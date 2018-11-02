https://docs.mongodb.com/manual/reference/operator/aggregation/arrayElemAt/#example
    .. code-block::

        from qmongo import qcollections
        users=qcollections.queryable(db,"users-11")
        ret,err =users.insert(
            [
                {"_id": 1, "name": "dave123", "favorites": ["chocolate", "cake", "butter", "apples"]},
                {"_id": 2, "name": "li", "favorites": ["apples", "pudding", "pie"]},
                {"_id": 3, "name": "ahn", "favorites": ["pears", "pecans", "chocolate", "cherries"]},
                {"_id": 4, "name": "ty", "favorites": ["ice cream"]}
            ]
        )

        """
           db.users.aggregate([
               {
                 $project:
                  {
                     name: 1,
                     first: { $arrayElemAt: [ "$favorites", 0 ] },
                     last: { $arrayElemAt: [ "$favorites", -1 ] }
                  }
               }
            ])
        """

        users.project(
            name=1,
            first="arrayElemAt(favorites,0)",
            last="arrayElemAt(favorites,-1)"
        )

        import pprint
        pprint.pprint(users.__pipe_line__)
        pprint.pprint(users.items)