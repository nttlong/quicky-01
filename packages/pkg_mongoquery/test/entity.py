import pymqr
from pymongo import MongoClient
cnn = MongoClient(
    host="localhost",
    port=27017
)
x=1
x>>=3
doc=pymqr.documents()
doc.name=int
doc.code=str

print doc.__dict__
db = cnn.get_database("hrm")
db.authenticate("root","123456")
items=pymqr.query(db,"employees").items
ret=pymqr.query(db,"emps").where(pymqr.doc.code >= 123)
pymqr.doc.name="dasd dsad dsad"
ret.set()
import pprint
pprint.pprint(ret)
