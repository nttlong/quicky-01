# encoding=utf8
import sys
import os
sys.path.append(os.getcwd()+os.sep+"packages")
from qmongo import qcollections
db1=qcollections.connect("lms",host="192.168.18.43",port=27017,name="lv_lms",user="root",password="123456")
db2=qcollections.connect("cs_lms",host="192.168.18.43",port=27017,name="lv_cs_comments_services",user="root",password="123456")
qr=qcollections.queryable(db.get_collection("modulestore.structures"))
