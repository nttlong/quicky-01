from pymongo import MongoClient
cnn=MongoClient(host="localhost",
                port=27017)
db=cnn.get_database("hrm")
db.authenticate(name="root",password="123456")

import pymqr
import pymmemberships.models.users
users=pymmemberships.models.users.users
x=pymqr.query(db,users).get_page(50,1)
print x.__dict__

