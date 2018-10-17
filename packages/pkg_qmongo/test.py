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

from qmongo import qcollections
inventory=qcollections.queryable(db,"inventory-22")
ret,err =inventory.insert(
    [
        {"_id": 1, "items": ["one", "two", "three"]},
        {"_id": 2, "items": [1, 2, 3]},
        {"_id": 3, "items": [None, None, 2]},
        {"_id": 4, "items": None},
        {"_id": 5, "amount": 3}
    ]
)

"""
db.inventory.aggregate(
   [
     {
       $project:
          {
            index: { $indexOfArray: [ "$items", 2 ] },
          }
      }
   ]
)
"""
inventory.project(
    index="indexOfArray(items,2)"
)

import pprint

pprint.pprint(inventory.__pipe_line__)
pprint.pprint(inventory.items)




