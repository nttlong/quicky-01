https://docs.mongodb.com/manual/reference/operator/aggregation/dateFromParts/#time-zone
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
              "nycHour": {
                 $hour: { date: "$date", timezone: "-05:00" }
               },
               "nycMinute": {
                  $minute: { date: "$date", timezone: "-05:00" }
               },
               "gmtHour": {
                  $hour: { date: "$date", timezone: "GMT" }
               },
               "gmtMinute": {
                  $minute: { date: "$date", timezone: "GMT" } },
               "nycOlsonHour": {
                  $hour: { date: "$date", timezone: "America/New_York" }
               },
               "nycOlsonMinute": {
                  $minute: { date: "$date", timezone: "America/New_York" }
               }
           }
        }])
        """
        sales.project(
            nycHour="hour(date,'-05:00')",
            nycMinute = "minute(date,'-05:00')",
            gmtHour="hour(date,'GMT')",
            gmtMinute="minute(date,'GMT')",
            nycOlsonHour="hour(date,'America/New_York')",
            nycOlsonMinute="minute(date,'America/New_York')"
        )

        import pprint

        pprint.pprint(sales.__pipe_line__)
        pprint.pprint(sales.items)

https://docs.mongodb.com/manual/reference/operator/aggregation/dateFromParts/#example
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
                 $dateFromParts: {
                    'year' : 2017, 'month' : 2, 'day': 8, 'hour' : 12
                 }
              },
              date_iso: {
                 $dateFromParts: {
                    'isoWeekYear' : 2017, 'isoWeek' : 6, 'isoDayOfWeek' : 3, 'hour' : 12
                 }
              },
              date_timezone: {
                 $dateFromParts: {
                    'year' : 2016, 'month' : 12, 'day' : 31, 'hour' : 23,
                    'minute' : 46, 'second' : 12, 'timezone' : 'America/New_York'
                 }
              }
           }
        }])
        """
        sales.project(
            date="dateFromParts(2017,2,0,12)",
            date_iso = "dateFromPartsWithISO(2017,6,3,12)",
            date_timezone="dateFromPartsWithTimeZone('America/New_York',2016,12,32,23,46,12)"
        )

        import pprint

        pprint.pprint(sales.__pipe_line__)
        pprint.pprint(sales.items)
