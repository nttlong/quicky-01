https://docs.mongodb.com/manual/reference/operator/aggregation/addFields/

.. code-block::

    data =[
    {
        "_id": 1,
        "student": "Maya",
        "homework": [10, 5, 10],
        "quiz": [10, 8],
        "extraCredit": 0
    },
    {
        "_id": 2,
        "student": "Ryan",
        "homework": [5, 6, 5],
        "quiz": [8, 8],
        "extraCredit": 8
    }
    ]
    from qmongo import qcollections
    scores=qcollections.queryable(db,"scores-4")
    ret,err =scores.insert(data)
    """
            db.scores.aggregate( [
           {
             $addFields: {
               totalHomework: { $sum: "$homework" } ,
               totalQuiz: { $sum: "$quiz" }
             }
           },
           {
             $addFields: { totalScore:
               { $add: [ "$totalHomework", "$totalQuiz", "$extraCredit" ] } }
           }
        ] )
    """

    agg=scores.add_fields(
        totalHomework="sum(homeWwork)"
    ).add_fields(
        totalScore="totalHomework+totalQuiz+extraCredit"
    )


    import pprint
    pprint.pprint(agg.__pipe_line__)
    pprint.pprint(agg.items)

Adding Fields to an Embedded Document
    .. code-block::

        data =[
            {"_id": 1, "type": "car", "specs": {"doors": 4, "wheels": 4}},
            {"_id": 2, "type": "motorcycle", "specs": {"doors": 0, "wheels": 2}},
            {"_id": 3, "type": "jet ski"}
        ]
        from qmongo import qcollections
        vehicles=qcollections.queryable(db,"vehicles-4")
        ret,err =vehicles.insert(data)
        """
               db.vehicles.aggregate( [
                {
                   $addFields: {
                      "specs.fuel_type": "unleaded"
                   }
                }
           ] )
        """

        agg=vehicles.add_fields(
            {
                "specs.fuel_type":"{0}"
            },"unleaded"
        )
        import pprint
        pprint.pprint(agg.__pipe_line__)
        pprint.pprint(agg.items)

Overwriting an existing field
    .. code-block::

        data =[
            {"_id": 1, "dogs": 10, "cats": 15}
        ]
        from qmongo import qcollections
        animals=qcollections.queryable(db,"animals-4")
        ret,err =animals.insert(data)
        """
               db.animals.aggregate( [
                  {
                    $addFields: { "cats": 20 }
                  }
                ] )
        """

        agg=animals.add_fields(
            dict(
                cats=20
            ),"unleaded"
        )
        import pprint
        pprint.pprint(agg.__pipe_line__)
        pprint.pprint(agg.items)


    .. code-block::

        data =[
            {"_id": 1, "item": "tangerine", "type": "citrus"},
            {"_id": 2, "item": "lemon", "type": "citrus"},
            {"_id": 3, "item": "grapefruit", "type": "citrus"}
        ]
        from qmongo import qcollections
        fruit=qcollections.queryable(db,"fruit-4")
        ret,err =fruit.insert(data)
        """
               db.fruit.aggregate( [
                  {
                    $addFields: {
                      _id : "$item",
                      item: "fruit"
                    }
                  }
                ] )
        """

        agg=fruit.add_fields(
            dict(
                _id="item",
                item="{0}"
            ),"fruit"
        )
        import pprint
        pprint.pprint(agg.__pipe_line__)
        pprint.pprint(agg.items)

