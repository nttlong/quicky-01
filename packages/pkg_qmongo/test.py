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
sales=qcollections.queryable(db,"sales-21")
ret,err =sales.insert(
    [
        dict(
            _id=0,
            items= [
                dict(item_id= 43, quantity= 2, price= 10),
                dict(item_id =2, quantity = 1, price =240)
            ]
        ),
        dict(
             _id = 1,
            items= [
                dict(item_id = 23, quantity = 3, price = 110),
                dict(item_id = 103, quantity = 4, price = 5),
                dict(item_id = 38, quantity = 1, price = 300)
            ]
        ),
        dict(
            _id = 2,
            items = [
                dict(item_id = 4, quantity = 1, price = 23)
            ]
        )

    ]
)

"""
db.sales.aggregate([
   {
      $project: {
         items: {
            $filter: {
               input: "$items",
               as: "item",
               cond: { $gte: [ "$$item.price", 100 ] }
            }
         }
      }
   }
])

"""
sales.project(
    items="filter(items,item,item.price>=100)"
)

import pprint

pprint.pprint(sales.__pipe_line__)
pprint.pprint(sales.items)




