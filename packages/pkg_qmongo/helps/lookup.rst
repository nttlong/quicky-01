Perform a Single Equality Join with $lookup
    https://docs.mongodb.com/manual/reference/operator/aggregation/lookup/#perform-a-single-equality-join-with-lookup

.. code-block::

    from qmongo import qcollections
    orders=qcollections.queryable(db,"orders-6")
    inventory=qcollections.queryable(db,"inventory-6")
    ret,err =orders.insert(
        [
           { "_id" : 1, "item" : "almonds", "price" : 12, "quantity" : 2 },
           { "_id" : 2, "item" : "pecans", "price" : 20, "quantity" : 1 },
           { "_id" : 3  }
        ]
    )
    ret,err =inventory.insert(
        [
            {"_id": 1, "sku": "almonds", "description": "product 1", "instock": 120},
            {"_id": 2, "sku": "bread", "description":"product 2", "instock": 80},
            {"_id": 3, "sku": "cashews", "description": "product 3", "instock": 60},
            {"_id": 4, "sku": "pecans", "description": "product 4", "instock": 70},
            {"_id": 5, "sku": None, "description": "Incomplete"},
            {"_id": 6}
        ]
    )
    """
        db.orders.aggregate([
           {
             $lookup:
               {
                 from: "inventory",
                 localField: "item",
                 foreignField: "sku",
                 as: "inventory_docs"
               }
          }
        ])
    """

    orders.lookup(
        source = orders,
        local_field="item",
        foreign_field="item",
        alias="inventory_docs"
    )

    import pprint
    pprint.pprint(orders.__pipe_line__)
    pprint.pprint(orders.items)

Use $lookup with an Array
    https://docs.mongodb.com/manual/reference/operator/aggregation/lookup/#use-lookup-with-an-array
    .. code-block::

        from qmongo import qcollections
        orders=qcollections.queryable(db,"orders-3")
        inventory=qcollections.queryable(db,"inventory-3")
        ret,err =orders.insert(
            [
                {"_id": 1, "item": "MON1003", "price": 350, "quantity": 2, "specs":
                    ["27 inch", "Retina display", "1920x1080"], "type": "Monitor"}
            ]
        )
        ret,err =inventory.insert(
            [
                {"_id": 1, "sku": "MON1003", "type": "Monitor", "instock": 120,
                 "size": "27 inch", "resolution": "1920x1080"},
                {"_id": 2, "sku": "MON1012", "type": "Monitor", "instock": 85,
                 "size": "23 inch", "resolution": "1280x800"},
                {"_id": 3, "sku": "MON1031", "type": "Monitor", "instock": 60,
                 "size": "23 inch", "display_type": "LED"}
            ]
        )
        """
                db.orders.aggregate([
                   {
                      $unwind: "$specs"
                   },
                   {
                      $lookup:
                         {
                            from: "inventory",
                            localField: "specs",
                            foreignField: "size",
                            as: "inventory_docs"
                        }
                   },
                   {
                      $match: { "inventory_docs": { $ne: [] } }
                   }
                ])
        """

        orders.unwind("specs").lookup(
            source = inventory,
            local_field="specs",
            foreign_field="size",
            alias="inventory_docs"
        ).match(
            "inventory_docs!=[]"
        )

        import pprint
        pprint.pprint(orders.__pipe_line__)
        pprint.pprint(orders.items)

Use $lookup with $mergeObjects
    https://docs.mongodb.com/manual/reference/operator/aggregation/lookup/#use-lookup-with-mergeobjects

