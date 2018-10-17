https://docs.mongodb.com/manual/reference/operator/aggregation/first/#example
    .. code-block::

        from qmongo import qcollections
        sales=qcollections.queryable(db,"sales-22")
        ret,err =sales.insert(
            [
                {"_id": 1, "item": "abc", "price": 10, "quantity": 2, "date": datetime.datetime(2014,01,01,8,00,00)},
                {"_id": 2, "item": "jkl", "price": 20, "quantity": 1, "date":  datetime.datetime(2014,02,03,9,00,00)},
                {"_id": 3, "item": "xyz", "price": 5, "quantity": 5, "date":  datetime.datetime(2014,02,03,9,05,00)},
                {"_id": 4, "item": "abc", "price": 10, "quantity": 10, "date":  datetime.datetime(2014,02,15,8,00,00)},
                {"_id": 5, "item": "xyz", "price": 5, "quantity": 10, "date":  datetime.datetime(2014,02,15,9,05,00)},
                {"_id": 6, "item": "xyz", "price": 5, "quantity": 5, "date":  datetime.datetime(2014,02,15,12,05,10)},
                {"_id": 7, "item": "xyz", "price": 5, "quantity": 10, "date":  datetime.datetime(2014,02,15,14,12,12)}
            ]
        )

        """
        db.sales.aggregate(
           [
             { $sort: { item: 1, date: 1 } },
             {
               $group:
                 {
                   _id: "$item",
                   firstSalesDate: { $first: "$date" }
                 }
             }
           ]
        )
        """
        sales.sort(
            item=1,
            date=1
        ).group(
            _id="item",
            selectors=dict(
                firstSalesDate="first(date)"
            )
        )

        import pprint

        pprint.pprint(sales.__pipe_line__)
        pprint.pprint(sales.items)