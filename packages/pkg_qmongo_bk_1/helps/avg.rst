Use in $group Stage
    https://docs.mongodb.com/manual/reference/operator/aggregation/avg/#use-in-group-stage
    .. code-block::

        import datetime
        from bson.objectid import ObjectId

        from qmongo import qcollections
        sales=qcollections.queryable(db,"sales-12")
        ret,err =sales.insert(
            [
                {"_id": 1, "item": "abc", "price": 10, "quantity": 2, "date": datetime.datetime(2014,1,1,8,0,0)},
                {"_id": 2, "item": "jkl", "price": 20, "quantity": 1, "date": datetime.datetime(2014,2,3,9)},
                {"_id": 3, "item": "xyz", "price": 5, "quantity": 5, "date": datetime.datetime(2014,2,3,9,5)},
                {"_id": 4, "item": "abc", "price": 10, "quantity": 10, "date": datetime.datetime(2014,2,15,8)},
                {"_id": 5, "item": "xyz", "price": 5, "quantity": 10, "date": datetime.datetime(2014,2,15,9,12,00)}
            ]
        )

        """
           db.sales.aggregate(
               [
                 {
                   $group:
                     {
                       _id: "$item",
                       avgAmount: { $avg: { $multiply: [ "$price", "$quantity" ] } },
                       avgQuantity: { $avg: "$quantity" }
                     }
                 }
               ]
            )
        """

        sales.group(
            _id="item",
            selectors=dict(
                avgAmount="avg(price*quntity)",
                avgQuantity="avg(quntity)"
            )
        )
        import pprint
        pprint.pprint(sales.__pipe_line__)
        pprint.pprint(sales.items)

Use in $project Stage
    https://docs.mongodb.com/manual/reference/operator/aggregation/avg/#use-in-project-stage
    .. code-block::

        from qmongo import qcollections
        students=qcollections.queryable(db,"students-12")
        ret,err =students.insert(
            [
                {"_id": 1, "quizzes": [10, 6, 7], "labs": [5, 8], "final": 80, "midterm": 75},
                {"_id": 2, "quizzes": [9, 10], "labs": [8, 8], "final": 95, "midterm": 80},
                {"_id": 3, "quizzes": [4, 5, 5], "labs": [6, 5], "final": 78, "midterm": 70}
            ]
        )

        """
           db.students.aggregate([
               {
                 $project: {
                   quizAvg: { $avg: "$quizzes"},
                   labAvg: { $avg: "$labs" },
                   examAvg: { $avg: [ "$final", "$midterm" ] }
                 }
               }
            ])
        """

        students.project(
            quizAvg="avg(quizzes)",
            labAvg="avg(labs)",
            examAvg="avg(final,midterm)"
        )
        import pprint
        pprint.pprint(students.__pipe_line__)
        pprint.pprint(students.items)
