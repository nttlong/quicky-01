https://docs.mongodb.com/manual/reference/operator/aggregation/cond/#example
    .. code-block::

        from qmongo import qcollections
        inventory=qcollections.queryable(db,"inventory-16")
        ret,err =inventory.insert(
            [
                {"_id": 1, "item": "abc1", "qty": 300},
                {"_id": 2, "item": "abc2", "qty": 200},
                {"_id": 3, "item": "xyz1", "qty": 250}
            ]
        )

        """
           db.inventory.aggregate(
               [
                  {
                     $project:
                       {
                         item: 1,
                         discount:
                           {
                             $cond: { if: { $gte: [ "$qty", 250 ] }, then: 30, else: 20 }
                           }
                       }
                  }
               ]
            )
        """

        inventory.project(
            item=1,
            discount="iif(qty>250,30,20)"
        )

        import pprint
        pprint.pprint(inventory.__pipe_line__)
        pprint.pprint(inventory.items)