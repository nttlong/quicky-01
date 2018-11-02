https://docs.mongodb.com/manual/reference/operator/aggregation/concatArrays/#example
    .. code-block::

        from qmongo import qcollections
        warehouses=qcollections.queryable(db,"warehouses-15")
        ret,err =warehouses.insert(
            [
                {"_id": 1, "instock": ["chocolate"], "ordered": ["butter", "apples"]},
                {"_id": 2, "instock": ["apples", "pudding", "pie"]},
                {"_id": 3, "instock": ["pears", "pecans"], "ordered": ["cherries"]},
                {"_id": 4, "instock": ["ice cream"], "ordered": []}
            ]
        )

        """
           db.warehouses.aggregate([
               { $project: { items: { $concatArrays: [ "$instock", "$ordered" ] } } }
            ])
        """

        warehouses.project(
            items="concatArrays(instock,ordered)"
        )

        import pprint
        pprint.pprint(warehouses.__pipe_line__)
        pprint.pprint(warehouses.items)
