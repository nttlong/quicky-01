import os
import sys
sys.path.append(os.getcwd()+os.sep+"packages")
import auth
import auth.models
import qmongo
qmongo.set_db_context("mongodb://root:123456@localhost:27017/hrm:hrm")