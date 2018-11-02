https://docs.mongodb.com/manual/reference/operator/aggregation/cmp/#example
    .. code-block::

        from qmongo import qcollections
        inventory=qcollections.queryable(db,"inventory-14")
        ret,err =inventory.insert(
            [
                {"_id": 1, "item": "abc1", "description": "product 1", "qty": 300},
                {"_id": 2, "item": "abc2", "description": "product 2", "qty": 200},
                {"_id": 3, "item": "xyz1", "description": "product 3", "qty": 250},
                {"_id": 4, "item": "VWZ1", "description": "product 4", "qty": 300},
                {"_id": 5, "item": "VWZ2", "description": "product 5", "qty": 180}
            ]
        )

        """
           db.inventory.aggregate(
               [
                 {
                   $project:
                      {
                        item: 1,
                        qty: 1,
                        cmpTo250: { $cmp: [ "$qty", 250 ] },
                        _id: 0
                      }
                 }
               ]
            )
        """

        inventory.project(
            item=1,
            qty=1,
            cmpTo250="cmp(qty,250)"
        )
        import pprint
        pprint.pprint(inventory.__pipe_line__)
        pprint.pprint(inventory.items)