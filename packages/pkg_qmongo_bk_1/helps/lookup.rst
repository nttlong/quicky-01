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

    .. code-block::

        from qmongo import qcollections
        orders=qcollections.queryable(db,"orders-7")
        items=qcollections.queryable(db,"items-7")
        ret,err =orders.insert(
            [
                {"_id": 1, "item": "almonds", "price": 12, "quantity": 2},
                {"_id": 2, "item": "pecans", "price": 20, "quantity": 1}
            ]
        )
        ret,err =items.insert(
            [
                {"_id": 1, "item": "almonds", "description": "almond clusters", "instock": 120},
                {"_id": 2, "item": "bread", "description": "raisin and nut bread", "instock": 80},
                {"_id": 3, "item": "pecans", "description": "candied pecans", "instock": 60}
            ]
        )
        """
            db.orders.aggregate([
               {
                  $lookup: {
                     from: "items",
                     localField: "item",    // field in the orders collection
                     foreignField: "item",  // field in the items collection
                     as: "fromItems"
                  }
               },
               {
                  $replaceRoot: { newRoot: { $mergeObjects: [ { $arrayElemAt: [ "$fromItems", 0 ] }, "$$ROOT" ] } }
               },
               { $project: { fromItems: 0 } }
            ])
        """

        orders.lookup(
            source = items,
            local_field="item",
            foreign_field="item",
            alias="fromItems"
        ).replace_root(
            "mergeObjects(arrayElemAt(fromItems,0),{0})" ,
            "$$ROOT"

        ).project(fromItems=0)

        import pprint
        pprint.pprint(orders.__pipe_line__)
        pprint.pprint(orders.items)

Specify Multiple Join Conditions with $lookup
    https://docs.mongodb.com/manual/reference/operator/aggregation/lookup/#specify-multiple-join-conditions-with-lookup

    .. code-block::

        from qmongo import qcollections
        orders=qcollections.queryable(db,"orders-8")
        warehouses=qcollections.queryable(db,"warehouses-8")
        ret,err =orders.insert(
            [
                {"_id": 1, "item": "almonds", "price": 12, "ordered": 2},
                {"_id": 2, "item": "pecans", "price": 20, "ordered": 1},
                {"_id": 3, "item": "cookies", "price": 10, "ordered": 60}
            ]
        )
        ret,err =warehouses.insert(
            [
                {"_id": 1, "stock_item": "almonds", "warehouse": "A", "instock": 120},
                {"_id": 2, "stock_item": "pecans", "warehouse": "A", "instock": 80},
                {"_id": 3, "stock_item": "almonds", "warehouse": "B", "instock": 60},
                {"_id": 4, "stock_item": "cookies", "warehouse": "B", "instock": 40},
                {"_id": 5, "stock_item": "cookies", "warehouse": "A", "instock": 80}
            ]
        )
        """
            db.orders.aggregate([
               {
                  $lookup:
                     {
                       from: "warehouses",
                       let: { order_item: "$item", order_qty: "$ordered" },
                       pipeline: [
                          { $match:
                             { $expr:
                                { $and:
                                   [
                                     { $eq: [ "$stock_item",  "$$order_item" ] },
                                     { $gte: [ "$instock", "$$order_qty" ] }
                                   ]
                                }
                             }
                          },
                          { $project: { stock_item: 0, _id: 0 } }
                       ],
                       as: "stockdata"
                     }
                }
            ])
        """

        orders.lookup(
            let=dict(
                order_item="item",
                order_qty = "ordered"
            ),
            source =warehouses ,
            pipeline=orders.create()
                .match("expr((stock_item=={1}) and (instock>={0}))","$$order_qty","$$order_item")
                .project(
                _id=0,
                stock_item=0
            ),
            alias="stockdata"
        )

        import pprint
        pprint.pprint(orders.__pipe_line__)
        pprint.pprint(orders.items)

Uncorrelated Subquery
    https://docs.mongodb.com/manual/reference/operator/aggregation/lookup/#uncorrelated-subquery

    .. code-block::

        import datetime
        from bson.objectid import ObjectId

        from qmongo import qcollections
        absences=qcollections.queryable(db,"absences-8")
        holidays=qcollections.queryable(db,"warehouses-8")
        ret,err =absences.insert(
            [
                {"_id": 1, "student": "Ann Aardvark", "sickdays": [datetime.datetime(2018,5,01), datetime.datetime(2018,8,23)]},
                {"_id": 2, "student": "Zoe Zebra", "sickdays": [datetime.datetime(2018,2,1), datetime.datetime(2018,5,23)]},
            ]
        )
        ret,err =holidays.insert(
            [
                {"_id": 1, "year": 2018, "name": "New Years", "date": datetime.datetime(2018,01,01)},
                {"_id": 2, "year": 2018, "name": "Pi Day", "date": datetime.datetime(2018,03,14)},
                {"_id": 3, "year": 2018, "name": "Ice Cream Day", "date": datetime.datetime(2018,07,15)},
                {"_id": 4, "year": 2017, "name": "New Years", "date": datetime.datetime(2017,01,01)},
                {"_id": 5, "year": 2017, "name": "Ice Cream Day", "date": datetime.datetime(2017,07,16)}
            ]
        )
        """
            db.absences.aggregate([
           {
              $lookup:
                 {
                   from: "holidays",
                   pipeline: [
                      { $match: { year: 2018 } },
                      { $project: { _id: 0, date: { name: "$name", date: "$date" } } },
                      { $replaceRoot: { newRoot: "$date" } }
                   ],
                   as: "holidays"
                 }
            }
        ])
        """

        absences.lookup(
            source =holidays ,
            pipeline=holidays.create()
                .match("year==2018")
                .project(
                _id=0,
                date=dict(
                    name="name",
                    date="date"
                )
            ).replace_root(
                "date"
            ),
            alias="holidays"
        )

        import pprint
        pprint.pprint(absences.__pipe_line__)
        pprint.pprint(absences.items)
