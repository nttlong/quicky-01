import sys
import os
sys.path.append(os.getcwd()+os.sep+"packages")
import config_reader
config_reader.load("local")
from quicky import tenancy
tenancy.set_schema("hrm")
from hrm.models import provinces