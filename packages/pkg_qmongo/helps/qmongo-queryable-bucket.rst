https://docs.mongodb.com/manual/reference/operator/aggregation/bucket/#example

.. code-block::

    data =[
    {"_id": 1, "title": "The Pillars of Society", "artist": "Grosz", "year": 1926,
     "price": 199.99},
    {"_id": 2, "title": "Melancholy III", "artist": "Munch", "year": 1902,
     "price": 280.00},
    {"_id": 3, "title": "Dancer", "artist": "Miro", "year": 1925,
     "price": 76.04},
    {"_id": 4, "title": "The Great Wave off Kanagawa", "artist": "Hokusai",
     "price": 167.30},
    {"_id": 5, "title": "The Persistence of Memory", "artist": "Dali", "year": 1931,
     "price": 483.00},
    {"_id": 6, "title": "Composition VII", "artist": "Kandinsky", "year": 1913,
     "price": 385.00},
    {"_id": 7, "title": "The Scream", "artist": "Munch", "year": 1893},
    {"_id": 8, "title": "Blue Flower", "artist": "O'Keefe", "year": 1918,
     "price": 118.42}
    ]
    from qmongo import qcollections
    artwork=qcollections.queryable(db,"artwork-5")
    ret,err =artwork.insert(data)
    """
           db.artwork.aggregate( [
              {
                $bucket: {
                  groupBy: "$price",
                  boundaries: [ 0, 200, 400 ],
                  default: "Other",
                  output: {
                    "count": { $sum: 1 },
                    "titles" : { $push: "$title" }
                  }
                }
              }
            ] )

    """

    agg=artwork.bucket(
        group_by="price",
        boundaries=[0,200,400],
        default="Other",
        output= dict(
            count="sum(1)",
            titles="push(title)"
        )
    )
    import pprint
    pprint.pprint(agg.__pipe_line__)
    pprint.pprint(agg.items)

Using $bucket with $facet
    .. code-block::

        data =[
        {"_id": 1, "title": "The Pillars of Society", "artist": "Grosz", "year": 1926,
         "price": 199.99},
        {"_id": 2, "title": "Melancholy III", "artist": "Munch", "year": 1902,
         "price": 280.00},
        {"_id": 3, "title": "Dancer", "artist": "Miro", "year": 1925,
         "price": 76.04},
        {"_id": 4, "title": "The Great Wave off Kanagawa", "artist": "Hokusai",
         "price": 167.30},
        {"_id": 5, "title": "The Persistence of Memory", "artist": "Dali", "year": 1931,
         "price": 483.00},
        {"_id": 6, "title": "Composition VII", "artist": "Kandinsky", "year": 1913,
         "price": 385.00},
        {"_id": 7, "title": "The Scream", "artist": "Munch", "year": 1893},
        {"_id": 8, "title": "Blue Flower", "artist": "O'Keefe", "year": 1918,
         "price": 118.42}
        ]
        from qmongo import qcollections
        artwork=qcollections.queryable(db,"artwork-5")
        ret,err =artwork.insert(data)
        """
               db.artwork.aggregate( [
                  {
                    $facet: {
                      "price": [
                        {
                          $bucket: {
                              groupBy: "$price",
                              boundaries: [ 0, 200, 400 ],
                              default: "Other",
                              output: {
                                "count": { $sum: 1 },
                                "artwork" : { $push: { "title": "$title", "price": "$price" } }
                              }
                          }
                        }
                      ],
                      "year": [
                        {
                          $bucket: {
                            groupBy: "$year",
                            boundaries: [ 1890, 1910, 1920, 1940 ],
                            default: "Unknown",
                            output: {
                              "count": { $sum: 1 },
                              "artwork": { $push: { "title": "$title", "year": "$year" } }
                            }
                          }
                        }
                      ]
                    }
                  }
                ] )

        """

        agg=artwork.facet(
            price=artwork.create().bucket(
                params=[dict(
                    title="title",
                    price="price"
                )],
                group_by="price",
                boundaries=[ 0, 200, 400 ],
                default="Other",
                output=dict(
                    count="sum(1)",
                    artwork="push({0})"
                )
            ),
            year = artwork.create().bucket(
                params=[dict(
                    title = "title",
                    year = "year"
                )],
                group_by="year",
                boundaries=[1890, 1910, 1920, 1940],
                default="Unkown",
                output=dict(
                    count="sum(1)",
                    artwork="push({0})"
                )
            )
        )
        import pprint
        pprint.pprint(agg.__pipe_line__)
        pprint.pprint(agg.items)
