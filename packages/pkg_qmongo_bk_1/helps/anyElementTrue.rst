https://docs.mongodb.com/manual/reference/operator/aggregation/anyElementTrue/#example
    .. code-block::

        from qmongo import qcollections
        survey=qcollections.queryable(db,"survey-11")
        ret,err =survey.insert(
            [
                {"_id": 1, "responses": [True]},
                {"_id": 2, "responses": [True, False]},
                {"_id": 3, "responses": []},
                {"_id": 4, "responses": [1, True, "seven"]},
                {"_id": 5, "responses": [0]},
                {"_id": 6, "responses": [[]]},
                {"_id": 7, "responses": [[0]]},
                {"_id": 8, "responses": [[False]]},
                {"_id": 9, "responses": [None]},
                {"_id": 10, "responses": [None]}
            ]
        )

        """
           db.survey.aggregate(
           [
             { $project: { responses: 1, isAnyTrue: { $anyElementTrue: [ "$responses" ] }, _id: 0 } }
           ]
        )
        """

        survey.project(
            responses=1,
            isAnyTrue="anyElementTrue(responses)",
            _id=0
        )

        import pprint
        pprint.pprint(survey.__pipe_line__)
        pprint.pprint(survey.items)
