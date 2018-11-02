https://docs.mongodb.com/manual/reference/operator/aggregation/dayOfMonth/#example

    .. code-block::

        import datetime
        from bson.objectid import ObjectId

        from qmongo import qcollections
        sales=qcollections.queryable(db,"sales-20")
        ret,err =sales.insert(
            [
                {
                    "_id": 1,
                    "item": "abc",
                    "price": 10,
                    "quantity": 2,
                    "date": datetime.datetime(2014,01,01,8,15,39,736)
                }

            ]
        )

        """
        db.sales.aggregate(
           [
             {
               $project:
                 {
                   year: { $year: "$date" },
                   month: { $month: "$date" },
                   day: { $dayOfMonth: "$date" },
                   hour: { $hour: "$date" },
                   minutes: { $minute: "$date" },
                   seconds: { $second: "$date" },
                   milliseconds: { $millisecond: "$date" },
                   dayOfYear: { $dayOfYear: "$date" },
                   dayOfWeek: { $dayOfWeek: "$date" },
                   week: { $week: "$date" }
                 }
             }
           ]
        )

        """
        sales.project(
            year="year(date)",
            month="month(date)",
            day="dayOfMonth(date)",
            dayOfMonthWithTimeZone="dayOfMonth(date,'-0400')",
            hour="hour(date)",
            minutes="minute(date)",
            second="second(date)",
            millisecond="millisecond(date)",
            dayOfYear="dayOfYear(date)",
            dayOfWeek="dayOfWeek(date)",
            dayOfWeekWithTimeZone="dayOfWeek(date,'-0400')",
            week="week(day)"
        )

        import pprint

        pprint.pprint(sales.__pipe_line__)
        pprint.pprint(sales.items)
