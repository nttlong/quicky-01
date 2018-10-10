# from . import settings
# import performance
# performance.api.models
#
# import django_db
# db=django_db.getdb()
#
# from pymongo import MongoClient
# cnn= MongoClient(
#     host="172.17.7.67",
#     port=27017
# )
# db=cnn.get_database("lms")
# if not db.authenticate("sys","123456"):
#     raise Exception("Loin kgong noi ket duoc")
#
#
# from qmongo.qcollections import queryable
# from django_db import getdb
# import qmongo
# import pymongo
# qr=queryable(getdb(),"MyTestCollection")
# ret,error =qr.where("code==@code",code="admin").pull(
#     "users.username=={0}","admin"
# ).commit()
# if error!= None:
#     print "Update data is error"
# else:
#     print "Update data is successful"
