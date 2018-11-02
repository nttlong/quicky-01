Unwind Array
    https://docs.mongodb.com/manual/reference/operator/aggregation/unwind/#unwind-array

    .. code-block::

        from qmongo import qcollections
        inventory=qcollections.queryable(db,"inventory-8")
        ret,err =inventory.insert(
            [
                {"_id": 1, "item": "ABC1", "sizes": ["S", "M", "L"]}
            ]
        )

        """
           db.inventory.aggregate( [ { $unwind : "$sizes" } ] )
        """

        inventory.unwind("sizes",preserve_null_and_empty_arrays=False)

        import pprint
        pprint.pprint(inventory.__pipe_line__)
        pprint.pprint(inventory.items)

includeArrayIndex and preserveNullAndEmptyArrays
    https://docs.mongodb.com/manual/reference/operator/aggregation/unwind/#includearrayindex-and-preservenullandemptyarrays

    .. code-block::

        from qmongo import qcollections
        inventory=qcollections.queryable(db,"inventory-9")
        ret,err =inventory.insert(
            [
                {"_id": 1, "item": "ABC", "sizes": ["S", "M", "L"]},
                {"_id": 2, "item": "EFG", "sizes": []},
                {"_id": 3, "item": "IJK", "sizes": "M"},
                {"_id": 4, "item": "LMN"},
                {"_id": 5, "item": "XYZ", "sizes": None}
            ]
        )

        """
           db.inventory.aggregate( [ { $unwind: { path: "$sizes", includeArrayIndex: "arrayIndex" } } ] )
        """

        inventory.unwind("sizes",
                         preserve_null_and_empty_arrays=False,
                         include_array_index="arrayIndex")

        import pprint
        pprint.pprint(inventory.__pipe_line__)
        pprint.pprint(inventory.items)

