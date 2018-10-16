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
orders=qcollections.queryable(db,"orders-3")
items=qcollections.queryable(db,"items-3")
ret,err =orders.insert(
    [
        {"_id": 1, "item": "almonds", "price": 12, "quantity": 2},
        {"_id": 2, "item": "pecans", "price": 20, "quantity": 1}
    ]
)
ret,err =items.insert(
    [
        {"_id": 1, "item": "almonds", "description": "almond clusters", "instock": 120},
        {"_id": 2, "item": "bread", "description": "raisin and nut bread", "instock": 80},
        {"_id": 3, "item": "pecans", "description": "candied pecans", "instock": 60}
    ]
)
"""
    db.orders.aggregate([
       {
          $lookup: {
             from: "items",
             localField: "item",    // field in the orders collection
             foreignField: "item",  // field in the items collection
             as: "fromItems"
          }
       },
       {
          $replaceRoot: { newRoot: { $mergeObjects: [ { $arrayElemAt: [ "$fromItems", 0 ] }, "$$ROOT" ] } }
       },
       { $project: { fromItems: 0 } }
    ])
"""

orders.lookup(
    source = items,
    local_field="item",
    foreign_field="item",
    alias="fromItems"
).replace_root(
    new_root = "$mergeObjects(arrayElemAt(fromItems,0),{0})",
    params =["$$ROOT"]

)

import pprint
pprint.pprint(orders.__pipe_line__)
pprint.pprint(orders.items)




