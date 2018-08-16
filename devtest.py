import sys
import os
sys.path.append(os.getcwd()+os.sep+"packages")
import config_reader
config_reader.load("local")
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
items = provinces.provinces().aggregate().project(
    code =1,
    name =1,
    description =1

).get_list()
xls.fetch_data(items)
from qexcel import readers
wb = readers.load_from_file("E:\\code\\quicky-01\\xls\\province.xlsx")

