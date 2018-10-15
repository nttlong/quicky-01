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
    {
        "_id": 1,
        "level": 1,
        "acct_id": "xyz123",
        "cc": {
            "level": 5,
            "type": "yy",
            "num": 000000000000,
            "exp_date": datetime.datetime(2015,11,1,0,0),
            "billing_addr": {
                "level": 5,
                "addr1": "123 ABC Street",
                "city": "Some City"
            },
            "shipping_addr": [
                {
                    "level": 3,
                    "addr1": "987 XYZ Ave",
                    "city": "Some City"
                },
                {
                    "level": 3,
                    "addr1": "PO Box 0123",
                    "city": "Some City"
                }
            ]
        },
        "status": "A"
    }
]
from qmongo import qcollections
accounts=qcollections.queryable(db,"accounts-4")
ret,err =accounts.insert(data)
"""
    db.accounts.aggregate(
      [
        { $match: { status: "A" } },
        {
          $redact: {
            $cond: {
              if: { $eq: [ "$level", 5 ] },
              then: "$$PRUNE",
              else: "$$DESCEND"
            }
          }
        }
      ]
    );
"""

agg=accounts.match("status=={0}","A")
agg.redact("iif(level=={0},{1},{2})",5,"$$PRUNE","$$DESCEND")

import pprint
pprint.pprint(agg.__pipe_line__)
pprint.pprint(agg.items)




