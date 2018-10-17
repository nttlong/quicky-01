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
sales=qcollections.queryable(db,"sales-20")
ret,err =sales.insert(
    [
        {
            "_id": 1,
            "item": "abc",
            "price": 10,
            "quantity": 2,
            "date": datetime.datetime(2014,01,01,8,15,39,736)
        }

    ]
)

"""
db.sales.aggregate(
   [
     {
       $project: {
          yearMonthDayUTC: { $dateToString: { format: "%Y-%m-%d", date: "$date" } },
          timewithOffsetNY: { $dateToString: { format: "%H:%M:%S:%L%z", date: "$date", timezone: "America/New_York"} },
          timewithOffset430: { $dateToString: { format: "%H:%M:%S:%L%z", date: "$date", timezone: "+04:30" } },
          minutesOffsetNY: { $dateToString: { format: "%Z", date: "$date", timezone: "America/New_York" } },
          minutesOffset430: { $dateToString: { format: "%Z", date: "$date", timezone: "+04:30" } }
       }
     }
   ]
)

"""
sales.project(
    ['$timezone','new Date(0)'],
    yearMonthDayUTC="dateToString(date,'%Y-%m-%d')",
    timewithOffsetNY="dateToString(date,'%H:%M:%S:%L%z','America/New_York')",
    timewithOffset430='dateToString(data,"%H:%M:%S:%L%z","+04:30")' ,
    minutesOffsetNY="dateToString(date,'%Z','America/New_York')",
    minutesOffset430="dateToString(data,'%Z','+04:30')",
)

import pprint

pprint.pprint(sales.__pipe_line__)
pprint.pprint(sales.items)




