https://docs.mongodb.com/manual/reference/operator/aggregation/add/#examples

    .. code-block::

        import datetime
        from bson.objectid import ObjectId

        from qmongo import qcollections
        sales=qcollections.queryable(db,"sales-9")
        ret,err =sales.insert(
            [
                {"_id": 1, "item": "abc", "price": 10, "fee": 2, "date": datetime.datetime(2014,3,1)},
                {"_id": 2, "item": "jkl", "price": 20, "fee": 1, "date": datetime.datetime(2014,3,1,9)},
                {"_id": 3, "item": "xyz", "price": 5, "fee": 0, "date": datetime.datetime(2014,3,15,9)}
            ]
        )

        """
           db.sales.aggregate(
               [
                 { $project: { item: 1, total: { $add: [ "$price", "$fee" ] } } }
               ]
           )
        """

        sales.project(
            item=1,
            total="price+fee"
        )

        import pprint
        pprint.pprint(sales.__pipe_line__)
        pprint.pprint(sales.items)

Perform Addition on a Date
    https://docs.mongodb.com/manual/reference/operator/aggregation/add/#perform-addition-on-a-date

    .. code-block::

        from qmongo import qcollections
        sales=qcollections.queryable(db,"sales-9")
        ret,err =sales.insert(
            [
                {"_id": 1, "item": "abc", "price": 10, "fee": 2, "date": datetime.datetime(2014,3,1)},
                {"_id": 2, "item": "jkl", "price": 20, "fee": 1, "date": datetime.datetime(2014,3,1,9)},
                {"_id": 3, "item": "xyz", "price": 5, "fee": 0, "date": datetime.datetime(2014,3,15,9)}
            ]
        )

        """
           db.sales.aggregate(
               [
                 { $project: { item: 1, billing_date: { $add: [ "$date", 3*24*60*60000 ] } } }
               ]
            )
        """

        sales.project(
            item=1,
            billing_date="date+3*24*60*60000"
        )

        import pprint
        pprint.pprint(sales.__pipe_line__)
        pprint.pprint(sales.items)

