https://docs.mongodb.com/manual/reference/operator/aggregation/collStats/

.. code-block::

    artwork=qcollections.queryable(db,"artwork-6")
    agg=artwork.coll_stats()
    import pprint
    pprint.pprint(agg.__pipe_line__)
    pprint.pprint(agg.items)