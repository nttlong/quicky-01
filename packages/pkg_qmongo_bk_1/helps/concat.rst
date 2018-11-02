https://docs.mongodb.com/manual/reference/operator/aggregation/concat/#examples
    .. code-block::

        from qmongo import qcollections
        inventory=qcollections.queryable(db,"inventory-15")
        ret,err =inventory.insert(
            [
                {"_id": 1, "item": "ABC1", "quarter": "13Q1", "description": "product 1"},
                {"_id": 2, "item": "ABC2", "quarter": "13Q4", "description": "product 2"},
                {"_id": 3, "item": "XYZ1", "quarter": "14Q2", "description": None}
            ]
        )

        """
           db.inventory.aggregate(
               [
                  { $project: { itemDescription: { $concat: [ "$item", " - ", "$description" ] } } }
               ]
            )
        """

        inventory.project(
            itemDescription="concat(item,'-',description)"
        )
        """
        if use it with params
        inventory.project(
        ['-'],
        itemDescription="concat(item,{0},description)"
        )
        """

        import pprint
        pprint.pprint(inventory.__pipe_line__)
        pprint.pprint(inventory.items)