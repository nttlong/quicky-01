https://docs.mongodb.com/manual/reference/operator/aggregation/addToSet/#example
    .. code-block::

        from qmongo import qcollections
        sales=qcollections.queryable(db,"sales-10")
        ret,err =sales.insert(
            [
                {"_id": 1, "item": "abc", "price": 10, "quantity": 2, "date": datetime.datetime(2014,1,1,8)},
                {"_id": 2, "item": "jkl", "price": 20, "quantity": 1, "date": datetime.datetime(2014,2,3,9)},
                {"_id": 3, "item": "xyz", "price": 5, "quantity": 5, "date": datetime.datetime(2014,2,3,9,05)},
                {"_id": 4, "item": "abc", "price": 10, "quantity": 10, "date": datetime.datetime(2014,2,15,8,00,00)},
                {"_id": 5, "item": "xyz", "price": 5, "quantity": 10, "date": datetime.datetime(2014,2,15,9,12,00)}
            ]
        )

        """
           db.sales.aggregate(
               [
                 {
                   $group:
                     {
                       _id: { day: { $dayOfYear: "$date"}, year: { $year: "$date" } },
                       itemsSold: { $addToSet: "$item" }
                     }
                 }
               ]
            )
        """

        sales.group(
            _id=dict(
                day="dayOfYear(date)",
                year="year(date)"),
            selectors=dict(
                itemSold="addToSet(item)"
            )
        )

        import pprint
        pprint.pprint(sales.__pipe_line__)
        pprint.pprint(sales.items)