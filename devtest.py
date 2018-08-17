import sys
import os
sys.path.append(os.getcwd()+os.sep+"packages")
import config_reader
config_reader.load("local")
# config_reader.load("server172_16_7_67")
from quicky import tenancy
tenancy.set_schema("hrm")
from hrm.models import provinces

from qexcel import writers
xls = writers.create(
    ("code","Code"),
    ("name","Name"),
    ("description","Description"),
    ("info.location.x","Location X"),
    ("info.location.y","Location Y"),
)
# items = provinces.provinces().aggregate().project(
#     code =1,
#     name =1,
#     description =1
#
# ).get_list()
# xls.fetch_data(items)
# from qexcel import readers
# wb = readers.load_from_file("/home/hcsadmin/q03/xls/province.xlsx")
# for x in wb.extract_data_as_list_of_object():
#     import pprint
#     ret=provinces.provinces().insert_one(x)
#     pprint.pprint(ret)

