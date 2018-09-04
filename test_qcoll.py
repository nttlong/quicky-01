# encoding=utf8
import sys
import os
sys.path.append(os.getcwd()+os.sep+"packages")
sys.path.append(os.getcwd()+os.sep+"packages/mongodb")
from qmongo import qcollections

db=qcollections.connect("local",host="localhost",port=27017,name="hrm",user="root",password="123456")
qr=qcollections.queryable(db.get_collection("test.emps"))
