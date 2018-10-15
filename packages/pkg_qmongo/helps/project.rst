Follow link https://docs.mongodb.com/manual/reference/operator/aggregation/project/
.It could be rewitre in qmongo like this:

    .. code-block::

        data =[
            {
              "_id" : 1,
              "title": "abc123",
              "isbn": "0001122223334",
              "author": { "last": "zzz", "first": "aaa" },
              "copies": 5
            }
        ]
        from qmongo import qcollections
        books=qcollections.queryable(db,"books-1")
        ret,err =books.insert(data)
        """
        db.books.aggregate( [ { $project : { title : 1 , author : 1 } } ] )

        """
        agg=books.project(title=1,author=1)
        import pprint
        pprint.pprint(agg.items)


    Conditionally Exclude Fields:

    .. code-block::

        import datetime
        data =[
            {
                "_id": 1,
                "title": "abc123",
                "isbn": "0001122223334",
                "author": {"last": "zzz", "first": "aaa"},
                "copies": 5,
                "lastModified": datetime.datetime(2016,07,28)
            },
            {
                "_id": 2,
                "title": "Baked Goods",
                "isbn": "9999999999999",
                "author": {"last": "xyz", "first": "abc", "middle": ""},
                "copies": 2,
                "lastModified": datetime.datetime(2017,07,21)
            },
            {
                "_id": 3,
                "title": "Ice Cream Cakes",
                "isbn": "8888888888888",
                "author": {"last": "xyz", "first": "abc", "middle": "mmm"},
                "copies": 5,
                "lastModified":datetime.datetime(2017,07,22)
            }
        ]
        from qmongo import qcollections
        books=qcollections.queryable(db,"books-2")
        ret,err =books.insert(data)
        """
        db.books.aggregate( [
           {
              $project: {
                 title: 1,
                 "author.first": 1,
                 "author.last" : 1,
                 "author.middle": {
                    $cond: {
                       if: { $eq: [ "", "$author.middle" ] },
                       then: "$$REMOVE",
                       else: "$author.middle"
                    }
                 }
              }
           }
        ] )

        """
        agg=books.project(["$$REMOVE"],title=1,author=dict(first=1,last=1,middle="iif(author.middle=='',{0},author.middle)"))
        import pprint
        pprint.pprint(agg.items)

    Include Specific Fields from Embedded Documents

    .. code-block::

        import datetime
        data =[
            {
                "_id": 1,
                "user": "1234",
                "stop": {
                    "title": "book1",
                    "author": "xyz",
                    "page": 32
                }
            },
            {
                "_id": 2,
                "user": "7890",
                "stop": [
                    {
                        "title": "book2",
                        "author": "abc",
                        "page": 5
                    },
                    {
                        "title": "book3",
                        "author": "ijk",
                        "page": 100
                    }
                ]
            }
        ]
        from qmongo import qcollections
        bookmarks=qcollections.queryable(db,"bookmarks-2")
        ret,err =bookmarks.insert(data)
        """
        db.bookmarks.aggregate( [ { $project: { stop: { title: 1 } } } ] )

        """
        agg=bookmarks.project(stop=dict(title=1))
        import pprint
        pprint.pprint(agg.items)

    Include Computed Fields:

    .. code-block::

        import datetime
        data =[
            {
                "_id": 1,
                "title": "abc123",
                "isbn": "0001122223334",
                "author": {"last": "zzz", "first": "aaa"},
                "copies": 5
            }
        ]
        from qmongo import qcollections
        books=qcollections.queryable(db,"books-3")
        ret,err =books.insert(data)
        """
        db.books.aggregate(
           [
              {
                 $project: {
                    title: 1,
                    isbn: {
                       prefix: { $substr: [ "$isbn", 0, 3 ] },
                       group: { $substr: [ "$isbn", 3, 2 ] },
                       publisher: { $substr: [ "$isbn", 5, 4 ] },
                       title: { $substr: [ "$isbn", 9, 3 ] },
                       checkDigit: { $substr: [ "$isbn", 12, 1] }
                    },
                    lastName: "$author.last",
                    copiesSold: "$copies"
                 }
              }
           ]
        )

        """
        agg=books.project(
            title=1,
            isbn=dict(
                prefix="substr(isbn,0,3)",
                group="substr(isbn,3,2)",
                publisher="substr(isbn,5,4)",
                title="substr(isbn,9,3)",
                checkDigit="substr(isbn,12,1)",
            ),
            lastName="author.last",
            copiesSold="copies"

        )
        import pprint
        pprint.pprint(agg.items)

    Project New Array Fields:

    .. code-block::

            import datetime
            import bson
            data =[
                {"_id": bson.objectid.ObjectId("55ad167f320c6be244eb3b95"), "x": 1, "y": 1}
            ]
            from qmongo import qcollections
            collection=qcollections.queryable(db,"collection-3")
            ret,err =collection.insert(data)
            """
            db.collection.aggregate( [ { $project: { myArray: [ "$x", "$y" ] } } ] )

            """
            agg=collection.project(
                myArray="[x,y]"
            )
            import pprint
            pprint.pprint(agg.items)

