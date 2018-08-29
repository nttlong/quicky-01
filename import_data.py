import devtest
from qmongo import json_file
import qmongo
import performance.api.models
colls =  [v for k,v in qmongo.models.__dict__.items() if k[0:3]=="HCS" or k in ["auth_user","auth_user_info"]]
qmongo.set_db_context("mongodb://sys:123456@172.16.7.67:27017/lms:nttlong")
for coll in colls:
    dir = "/home/hcsadmin/q03/json_data"
    filename = coll.coll._none_schema_name+".json"
    json_file.import_from(coll,dir+"/"+filename)
