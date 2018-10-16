https://docs.mongodb.com/manual/reference/operator/aggregation/redact/

    ..  code-block::

        data =[
        {
            "_id": 1,
            "title": "123 Department Report",
            "tags": ["G", "STLW"],
            "year": 2014,
            "subsections": [
                {
                    "subtitle": "Section 1: Overview",
                    "tags": ["SI", "G"],
                    "content": "Section 1: This is the content of section 1."
                },
                {
                    "subtitle": "Section 2: Analysis",
                    "tags": ["STLW"],
                    "content": "Section 2: This is the content of section 2."
                },
                {
                    "subtitle": "Section 3: Budgeting",
                    "tags": ["TK"],
                    "content": {
                        "text": "Section 3: This is the content of section3.",
                        "tags": ["HCS"]
                    }
                }
                ]
            }
        ]
        from qmongo import qcollections
        forecasts=qcollections.queryable(db,"forecasts-4")
        ret,err =forecasts.insert(data)
        """
            var userAccess = [ "STLW", "G" ];
            db.forecasts.aggregate(
               [
                 { $match: { year: 2014 } },
                 { $redact: {
                    $cond: {
                       if: { $gt: [ { $size: { $setIntersection: [ "$tags", userAccess ] } }, 0 ] },
                       then: "$$DESCEND",
                       else: "$$PRUNE"
                     }
                   }
                 }
               ]
            );
        """
        userAccess = ["STLW", "G"]

        agg=forecasts.match("year=={0}",2014)
        agg.redact("iif(size(setIntersection(tags,{0}))>0,{1},{2})",userAccess,"$$DESCEND","$$PRUNE")

        import pprint
        pprint.pprint(agg.items)

Exclude All Fields at a Given Level:

    .. code-block::

        import datetime
        from bson.objectid import ObjectId
        data =[
            {
                "_id": 1,
                "level": 1,
                "acct_id": "xyz123",
                "cc": {
                    "level": 5,
                    "type": "yy",
                    "num": 000000000000,
                    "exp_date": datetime.datetime(2015,11,1,0,0),
                    "billing_addr": {
                        "level": 5,
                        "addr1": "123 ABC Street",
                        "city": "Some City"
                    },
                    "shipping_addr": [
                        {
                            "level": 3,
                            "addr1": "987 XYZ Ave",
                            "city": "Some City"
                        },
                        {
                            "level": 3,
                            "addr1": "PO Box 0123",
                            "city": "Some City"
                        }
                    ]
                },
                "status": "A"
            }
        ]
        from qmongo import qcollections
        accounts=qcollections.queryable(db,"accounts-4")
        ret,err =accounts.insert(data)
        """
            db.accounts.aggregate(
              [
                { $match: { status: "A" } },
                {
                  $redact: {
                    $cond: {
                      if: { $eq: [ "$level", 5 ] },
                      then: "$$PRUNE",
                      else: "$$DESCEND"
                    }
                  }
                }
              ]
            );
        """

        agg=accounts.match("status=={0}","A")
        agg.redact("iif(level=={0},{1},{2})",5,"$$PRUNE","$$DESCEND")

        import pprint
        pprint.pprint(agg.__pipe_line__)
        pprint.pprint(agg.items)
