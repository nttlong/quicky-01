from pymongo import MongoClient
cnn=MongoClient(host="localhost",
                port=27017)
db=cnn.get_database("hrm")
db.authenticate(name="root",password="123456")

import pymqr
import pymmemberships.models.users
from pymqr import pydoc
users=pymmemberships.models.users.users
user= {
    users.Username:"system",
    users.PasswordSalt:"12344",
    users.HashPassword:"ddsada",

}
ret=pymqr.query(db,users).insert(user).commit()
print ret
filter = pydoc.filters.Name=="123"
# filter = filter | "name==123"
# import datetime
# items=pymqr.query(db,users).where(
#     pymqr.funcs.expr(users.Logins(5).SessionID=="123456")
# ).pull(pymqr.docs.SessionID=="12345").commit()
print pydoc.filters.to_mongodb()





