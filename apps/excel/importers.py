import openpyxl
class excel_name_range(object):
    def __init__(self):

        self.name=None
        self.address=None
        self.col = -1



class excel_config(object):
    def __init__(self):
        self.names=[]
        self.data_sheet=None
        self.workbook=None
    def get_data_template(self):
        ret_data ={}
        ret=ret_data
        for x in self.names:
            ret=ret_data
            if x.name.split('.').__len__() ==1:
                ret.update({x.name: (x.name, x.col)})
            else:
                for y in x.name.split('.'):
                    if not ret.has_key(y):
                        if x.name.split('.').index(y)==x.name.split('.').__len__()-1:
                            ret.update({y:(x.name , x.col)})
                        else:
                            ret.update({y:{}})
                            ret=ret[y]
        return ret_data
def load_from_file(file):
    ret = excel_config()
    file = open(file, 'rb')
    wb = openpyxl.load_workbook(filename=file)
    ws_data =[ws for ws in wb.worksheets if ws.title =="data"]
    if ws_data.__len__()==0:
        raise (Exception("Invalid workbook. The workbook must contains one worksheet with name is 'data'"))
    ret.workbook=wb
    ret.data_sheet=ws_data[0]
    ret.names=[]
    for x in wb.defined_names.definedName:
        from openpyxl.utils import coordinate_from_string, column_index_from_string
        if hasattr(x,"name"):
            item= excel_name_range()
            item.address=x.value
            item.name=x.name
            item.col=coordinate_from_string(x.value.split("!")[1].split(":")[0].replace("$","")+"1")[1]
            ret.names.append(item)

    ret.names = sorted(ret.names, key=lambda x: x.name)
    return ret

