https://docs.mongodb.com/manual/reference/operator/aggregation/ceil/#example
.. code-block::

    from qmongo import qcollections
    samples=qcollections.queryable(db,"samples-12")
    ret,err =samples.insert(
        [
            {"_id": 1, "value": 9.25},
            {"_id": 2, "value": 8.73},
            {"_id": 3, "value": 4.32},
            {"_id": 4, "value": -5.34}
        ]
    )

    """
       db.samples.aggregate([
           { $project: { value: 1, ceilingValue: { $ceil: "$value" } } }
        ])
    """

    samples.project(
        value=1,
        ceilingValue="ceil(value)"
    )
    import pprint
    pprint.pprint(samples.__pipe_line__)
    pprint.pprint(samples.items)