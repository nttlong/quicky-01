from __future__ import division
import openpyxl
import xlrd
import datetime
import trollius
from trollius import tasks
from openpyxl.utils import coordinate_from_string, column_index_from_string


class __obj__(object):
    pass
t1= datetime.datetime.now()
fx = xlrd.open_workbook("/home/hcsadmin/q03/xls/a001.xlsx")
cols_2 = []
for k,v in fx.name_and_scope_map.items():
    col = __obj__()
    col.name = v.name
    col.address = v.formula_text
    col.cell_letter = v.formula_text.split('!')[1].split(':')[0].split('$')[1]
    col.index = column_index_from_string(col.cell_letter)
    cols_2.append(col)
data_sheet_2 = [x for x in fx.sheets() if x.name == "data"][0]
data =[]
def get_row():
    @trollius.coroutine
    def get_cell(x,y):
        cell = data_sheet_2.cell(x,y)
        if cell.data_type == 1:
            return cell.value
        if cell.data_type == 2:
            return cell.value
        if cell.data_type == 3:
            return datetime.datetime(*xlrd.xldate_as_tuple(cell.value, fx.datemode))

    ret = []
    @tasks.coroutine
    def create_row(row):
        for i in range(0,data_sheet_2.ncols):
            ret.append(get_cell(row,i))
        return ret
    @trollius.coroutine
    def fetch():
        for row in range(1, data_sheet_2.nrows):
            yield create_row(data_sheet_2.row(row))
    loop =trollius.get_event_loop()
    loop.run_until_complete(fetch())
    return fetch()
t2 = datetime.datetime.now()
n2= (t2 - t1).microseconds
t1= datetime.datetime.now()
# wb=openpyxl.load_workbook("/home/hcsadmin/q03/xls/a001.xlsx")
# cols_1 =[]
# for x in wb.defined_names.definedName:
#
#     if hasattr(x, "name") and x.value != 'data!#REF!':
#         item = __obj__()
#         item.address = x.value
#         item.name = x.name
#         item.col = column_index_from_string(x.value.split("!")[1].split(":")[0].replace("$", "")) - 1
#         cols_1.append(item)
# data_sheet_1 = wb.get_sheet_by_name("data")
# t2 = datetime.datetime.now()
# n1= (t2 - t1).microseconds
# wb.close()
# get_row_time_1 = datetime.datetime.now()
# list(data_sheet_1.rows)
# get_row_time_1 = (datetime.datetime.now()-get_row_time_1).microseconds
#
# get_row_time_2 = datetime.datetime.now()
# list(get_row())
# get_row_time_2 = (datetime.datetime.now()-get_row_time_2).microseconds



