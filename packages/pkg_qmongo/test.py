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
inventory=qcollections.queryable(db,"inventory-12")
ret,err =inventory.insert(
    [
        {"_id": 1, "item": "ABC1", "instock": {"warehouse1": 2500, "warehouse2": 500}},
        {"_id": 2, "item": "ABC2", "instock": {"warehouse2": 500, "warehouse3": 200}}
    ]
)

"""
   db.inventory.aggregate( [
       { $addFields: { instock: { $objectToArray: "$instock" } } },
       { $addFields: { instock: { $concatArrays: [ "$instock", [ { "k": "total", "v": { $sum: "$instock.v" } } ] ] } } } ,
       { $addFields: { instock: { $arrayToObject: "$instock" } } }
    ] )
"""

inventory.add_fields(
    instock="objectToArray(instock)"
).add_fields(
    [ inventory.compile(
        dict(
            k="{0}",
            v="sum(instock.v)"
        ),"total"
    )],
    instock="concatArrays(instock,{0})",
).add_fields(
    instock = "arrayToObject(instock)"
)

import pprint
pprint.pprint(inventory.__pipe_line__)
pprint.pprint(inventory.items)




