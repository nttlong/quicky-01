import compilers
import pyquery
import pymongo
from pymongo import MongoClient
import pyfuncs
import pydoc
X=pydoc.Fields()
print pyfuncs.toDouble(X.name)
# fields=pydoc.Fields()
# x=pyfuncs.cmp(fields.amount,fields.name)==0
# print isinstance(x,pydoc.Fields)
# # c=x.__owner__
# print x.__tree__
# cnn=MongoClient(host="localhost",
#                 port=27017)
# db=cnn.get_database("lms")
# db.authenticate(name="sys",password="12345")
# qr=pyquery.query(db,"test.coll001")
# qr=qr+2
#     #.set(x=1,y=2)
# import pprint
# items=list(qr.objects)
# pprint.pprint(list(qr.find_to_objects()))

# ret=qr=pyquery.query(db,"test.coll001").insert(dict(
#     name=1
# ),dict(
#     fx="312313"
# )).commit()
# print ret
# qr=pyquery.query(db,"test").lookup(
#     From="ddd",
#     locaField="vvv",
#     foriegbField="ggg",
#     alias="ggg"
#
# ).lookup(
#     From="bbb",
#     pipeline="bbbb",
#     let="bbbb",
#     alias="bbbbb",
#
# )


# import expression_parser
# x=expression_parser.to_mongobd("x=={0}",'aaa')
# # expr,params=expression_parser.parse("$x==@test1",test1=2,username='admin')
# print qr.pipeline
#print params