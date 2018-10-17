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
fruit=qcollections.queryable(db,"fruit-22")
ret,err =fruit.insert(
    [
        {"_id": 1, "location": "24th Street",
         "in_stock": ["apples", "oranges", "bananas"]},
        {"_id": 2, "location": "36th Street",
         "in_stock": ["bananas", "pears", "grapes"]},
        {"_id": 3, "location": "82nd Street",
         "in_stock": ["cantaloupes", "watermelons", "apples"]}
    ]
)

"""
db.fruit.aggregate([
  {
    $project: {
      "store location" : "$location",
      "has bananas" : {
        $in: [ "bananas", "$in_stock" ]
      }
    }
  }
])
"""
fruit.project(
    store_location="location",
    has_bananas = "_in('bananas',in_stock)"

)

import pprint

pprint.pprint(fruit.__pipe_line__)
pprint.pprint(fruit.items)




