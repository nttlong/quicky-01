from networkx.algorithms import boundary

import qmongo
db=qmongo.connect(
    host="localhost",
    port=27017,
    name="hrm",
    user="root",
    password="123456"
)
import datetime
from bson.objectid import ObjectId
data =[
    {"_id": 1, "subject": "History", "score": 88},
    {"_id": 2, "subject": "History", "score": 92},
    {"_id": 3, "subject": "History", "score": 97},
    {"_id": 4, "subject": "History", "score": 71},
    {"_id": 5, "subject": "History", "score": 79},
    {"_id": 6, "subject": "History", "score": 83}
]
from qmongo import qcollections
scores=qcollections.queryable(db,"scores-6")
ret,err =scores.insert(data)
"""
   db.scores.aggregate(
  [
    {
      $match: {
        score: {
          $gt: 80
        }
      }
    },
    {
      $count: "passing_scores"
    }
  ]
)

"""

agg=scores.match("score>80").count("passing_scores")
import pprint
pprint.pprint(agg.__pipe_line__)
pprint.pprint(agg.items)




