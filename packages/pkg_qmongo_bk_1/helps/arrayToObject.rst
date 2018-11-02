https://docs.mongodb.com/manual/reference/operator/aggregation/arrayToObject/#arraytoobject-example
    .. code-block::

        from qmongo import qcollections
        inventory=qcollections.queryable(db,"inventory-11")
        ret,err =inventory.insert(
            [
                {"_id": 1, "item": "ABC1", "dimensions": [{"k": "l", "v": 25}, {"k": "w", "v": 10}, {"k": "uom", "v": "cm"}]},
                {"_id": 2, "item": "ABC2", "dimensions": [["l", 50], ["w", 25], ["uom", "cm"]]},
                {"_id": 3, "item": "ABC3", "dimensions": [["l", 50], ["l", 25], ["l", "cm"]]}
            ]
        )

        """
           db.inventory.aggregate(
               [
                  {
                     $project: {
                        item: 1,
                        dimensions: { $arrayToObject: "$dimensions" }
                     }
                  }
               ]
            )
        """

        inventory.project(
            item=1,
            dimensions="arrayToObject(dimensions)"
        )

        import pprint
        pprint.pprint(inventory.__pipe_line__)
        pprint.pprint(inventory.items)

$objectToArray + $arrayToObject
    https://docs.mongodb.com/manual/reference/operator/aggregation/arrayToObject/#objecttoarray-arraytoobject-example
        .. code-block::

            from qmongo import qcollections
            inventory=qcollections.queryable(db,"inventory-12")
            ret,err =inventory.insert(
                [
                    {"_id": 1, "item": "ABC1", "instock": {"warehouse1": 2500, "warehouse2": 500}},
                    {"_id": 2, "item": "ABC2", "instock": {"warehouse2": 500, "warehouse3": 200}}
                ]
            )

            """
               db.inventory.aggregate( [
                   { $addFields: { instock: { $objectToArray: "$instock" } } },
                   { $addFields: { instock: { $concatArrays: [ "$instock", [ { "k": "total", "v": { $sum: "$instock.v" } } ] ] } } } ,
                   { $addFields: { instock: { $arrayToObject: "$instock" } } }
                ] )
            """

            inventory.add_fields(
                instock="objectToArray(instock)"
            ).add_fields(
                [ inventory.compile(
                    dict(
                        k="{0}",
                        v="sum(instock.v)"
                    ),"total"
                )],
                instock="concatArrays(instock,{0})",
            ).add_fields(
                instock = "arrayToObject(instock)"
            )

            import pprint
            pprint.pprint(inventory.__pipe_line__)
            pprint.pprint(inventory.items)