from pymongo import MongoClient
cnn=MongoClient(host="localhost",
                port=27017)
db=cnn.get_database("hrm")
db.authenticate(name="root",password="123456")
import pymqr
import pymmemberships.models.users
from pymqr import pydoc
import pymmemberships.users
ret = pymmemberships.users.create({
    "Username":"XXX",
    "LastName":"XXX",
    "PasswordSalt":"XX",
    "Email":"XX",
    "HashPassword":"XX"
})
m=ret
# users=pymmemberships.models.users.users
# if {users.Profile.B# users=pymmemberships.models.users.users
# if {users.Profile.BirthDate.Code,"Username"} in users:
#     print "A"
# irthDate.Code,"Username"} in users:
#     print "A"


# x=users()
# x=users<<dict(
#     Username="system",
#     PasswordSalt="dsad",
#     Email = "dasdas",
#     HashPassword= "dasdas"
#
# )
# x.doc()
# user= {
#     users.Username:"system",
#     users.PasswordSalt:"12344",
#     users.HashPassword:12345,
#
# }
# print x.filter().Username==1

# ret=pymqr.query(db,users).insert(user).commit()
# print ret
# filter = pydoc.filters.Name=="123"
# # filter = filter | "name==123"
# # import datetime
# # items=pymqr.query(db,users).where(
# #     pymqr.funcs.expr(users.Logins(5).SessionID=="123456")
# # ).pull(pymqr.docs.SessionID=="12345").commit()
# print pydoc.filters.to_mongodb()





