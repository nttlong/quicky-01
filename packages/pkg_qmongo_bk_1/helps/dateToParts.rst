https://docs.mongodb.com/manual/reference/operator/aggregation/dateToParts/#example
    .. code-block::

        from qmongo import qcollections
        sales=qcollections.queryable(db,"sales-18")
        ret,err =sales.insert(
            [
                {
                    "_id": 1,
                    "item": "abc",
                    "price": 20,
                    "quantity": 5,
                    "date": datetime.datetime(2017,5,20,10,24,51,303)
                }

            ]
        )

        """
        db.sales.aggregate([
         {
            $project: {
               date: {
                  $dateToParts: { date: "$date" }
               },
               date_iso: {
                  $dateToParts: { date: "$date", iso8601: true }
               },
               date_timezone: {
                  $dateToParts: { date: "$date", timezone: "America/New_York" }
               }
            }
        }])
        """
        sales.project(
            ['America/New_York',2017],
            date="dateToParts(date)",
            date_iso = "dateToPartsWithISO8601(date)",
            date_timezone="dateToPartsWithTimeZone(date,{0})"
        )

        import pprint

        pprint.pprint(sales.__pipe_line__)
        pprint.pprint(sales.items)


