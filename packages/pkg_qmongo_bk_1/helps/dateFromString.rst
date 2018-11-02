https://docs.mongodb.com/manual/reference/operator/aggregation/dateFromString/#examples
    .. code-block::

            from qmongo import qcollections
        logmessages=qcollections.queryable(db,"logmessages-18")
        ret,err =logmessages.insert(
            [
                {"_id": 1, "date": "2017-02-08T12:10:40.787", "timezone": "America/New_York", "message": "Step 1: Started"},
                {"_id": 2, "date": "2017-02-08", "timezone": "-05:00", "message": "Step 1: Ended"},
                {"_id": 3, "message": " Step 1: Ended "},
                {"_id": 4, "date": "2017-02-09", "timezone": "Europe/London", "message": "Step 2: Started"},
                {"_id": 5, "date": "2017-02-09T03:35:02.055", "timezone": "+0530", "message": "Step 2: In Progress"}

            ]
        )

        """
        db.logmessages.aggregate( [ {
           $project: {
              date: {
                 $dateFromString: {
                    dateString: '$date',
                    timezone: 'America/New_York'
                 }
              }
           }
        } ] )

        """
        logmessages.project(
            ['America/New_York',2017],
            date="dateFromString(date,{0})"
        )

        import pprint

        pprint.pprint(logmessages.__pipe_line__)
        pprint.pprint(logmessages.items)


    .. code-block::

        """
        db.logmessages.aggregate( [ {
           $project: {
              date: {
                 $dateFromString: {
                    dateString: '$date',
                    timezone: '$timezone'
                 }
              }
           }
        } ] )

        """
        logmessages.project(
            ['$timezone'],
            date="dateFromString(date,{0})"
        )

onError
    https://docs.mongodb.com/manual/reference/operator/aggregation/dateFromString/#onerror
        .. code-block::

            from qmongo import qcollections
            dates=qcollections.queryable(db,"dates-18")
            ret,err =dates.insert(
                [
                    {"_id": 1, "date": "2017-02-08T12:10:40.787", "timezone": "America/New_York"},
                    {"_id": 2, "date": "20177-02-09T03:35:02.055", "timezone": "America/New_York"}

                ]
            )

            """
            db.dates.aggregate( [ {
               $project: {
                  date: {
                     $dateFromString: {
                        dateString: '$date',
                        timezone: '$timezone',
                        onError: '$date'
                     }
                  }
               }
            } ] )

            """
            dates.project(
                ['$timezone','$date'],
                date="dateFromString(date,{0},None,{1})"
            )

            import pprint

onNull
    https://docs.mongodb.com/manual/reference/operator/aggregation/dateFromString/#onnull
    .. code-block::

        ret,err =dates.insert(
            [
                {"_id": 1, "date": "2017-02-08T12:10:40.787", "timezone": "America/New_York"},
                {"_id": 2, "date": "20177-02-09T03:35:02.055", "timezone": "America/New_York"}

            ]
        )

        """
        db.dates.aggregate( [ {
           $project: {
              date: {
                 $dateFromString: {
                    dateString: '$date',
                    timezone: '$timezone',
                    onNull: new Date(0)
                 }
              }
           }
        } ] )

        """
        dates.project(
            ['$timezone','new Date(0)'],
            date="dateFromString(date,{0},{1})"
        )

        import pprint

        pprint.pprint(dates.__pipe_line__)
        pprint.pprint(dates.items)