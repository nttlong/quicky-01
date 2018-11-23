from pymongo import MongoClient
cnn=MongoClient(host="localhost",
                port=27017)
db=cnn.get_database("hrm")
db.authenticate(name="root",password="123456")
from pymqr import settings
settings.setdb(db)
import pymqr
import pymmemberships.models.users
from pymqr import pydocs
import pymmemberships.users
ret = pymmemberships.users.create(
    username="sys",
    password="sys",
    email="XXX"
)
pymmemberships.users.login("XXXX",123)

