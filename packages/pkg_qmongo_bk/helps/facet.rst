https://docs.mongodb.com/manual/reference/operator/aggregation/facet/#pipe._S_facet

.. code-block::

    data =[
    {"_id": 1, "title": "The Pillars of Society", "artist": "Grosz", "year": 1926,
     "price": 199.99,
     "tags": ["painting", "satire", "Expressionism", "caricature"]},
    {"_id": 2, "title": "Melancholy III", "artist": "Munch", "year": 1902,
     "price": 280.00,
     "tags": ["woodcut", "Expressionism"]},
    {"_id": 3, "title": "Dancer", "artist": "Miro", "year": 1925,
     "price": 76.04,
     "tags": ["oil", "Surrealism", "painting"]},
    {"_id": 4, "title": "The Great Wave off Kanagawa", "artist": "Hokusai",
     "price": 167.30,
     "tags": ["woodblock", "ukiyo-e"]},
    {"_id": 5, "title": "The Persistence of Memory", "artist": "Dali", "year": 1931,
     "price": 483.00,
     "tags": ["Surrealism", "painting", "oil"]},
    {"_id": 6, "title": "Composition VII", "artist": "Kandinsky", "year": 1913,
     "price": 385.00,
     "tags": ["oil", "painting", "abstract"]},
    {"_id": 7, "title": "The Scream", "artist": "Munch", "year": 1893,
     "tags": ["Expressionism", "painting", "oil"]},
    {"_id": 8, "title": "Blue Flower", "artist": "O'Keefe", "year": 1918,
     "price": 118.42,
     "tags": ["abstract", "painting"]}
    ]
    from qmongo import qcollections
    artwork=qcollections.queryable(db,"artwork-4")
    ret,err =artwork.insert(data)
    """
           db.artwork.aggregate( [
          {
            $facet: {
              "categorizedByTags": [
                { $unwind: "$tags" },
                { $sortByCount: "$tags" }
              ],
              "categorizedByPrice": [
                // Filter out documents without a price e.g., _id: 7
                { $match: { price: { $exists: 1 } } },
                {
                  $bucket: {
                    groupBy: "$price",
                    boundaries: [  0, 150, 200, 300, 400 ],
                    default: "Other",
                    output: {
                      "count": { $sum: 1 },
                      "titles": { $push: "$title" }
                    }
                  }
                }
              ],
              "categorizedByYears(Auto)": [
                {
                  $bucketAuto: {
                    groupBy: "$year",
                    buckets: 4
                  }
                }
              ]
            }
          }
        ])
    """

    agg=artwork.facet(
        categorizedByTags=artwork.create()
            .unwind("tags")
            .sort_by_count("tags"),
        categorizedByPrice=artwork.create()
            .match("exists(price)")
            .bucket(
            params=[1],
            group_by="price",
            boundaries=[0, 150, 200, 300, 400],
            default="Other",
            output=dict(
                count="sum({0})",
                titles="push(title)"
            )),
        categorizedByYears_Auto=artwork.create()
            .bucket_auto(
            group_by="year",
            buckets=4)
    )
    import pprint
    pprint.pprint(agg.__pipe_line__)
    pprint.pprint(agg.items)
