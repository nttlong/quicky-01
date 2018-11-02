https://docs.mongodb.com/manual/reference/operator/aggregation/and/#example
    .. code-block::

        from qmongo import qcollections
        inventory=qcollections.queryable(db,"inventory-10")
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
                    result: { $and: [ { $gt: [ "$qty", 100 ] }, { $lt: [ "$qty", 250 ] } ] }
                  }
             }
           ]
        )
        """

        inventory.project(
            item=1,
            qty=1,
            result="qty>100 and qty<250"
        )

        import pprint
        pprint.pprint(inventory.__pipe_line__)
        pprint.pprint(inventory.items)
