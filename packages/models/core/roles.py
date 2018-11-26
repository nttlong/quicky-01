from pymqr import documents
import datetime
@documents.EmbededArray()
class RolePrivileges(object):
    def __init__(self):
        self.Function_id=str
        self.Read=str
        self.Create=str
        self.Write=str
        self.Delete=str
        self.Export=str
        self.Import=str
        self.Copy=str
        self.Attach=str
        self.Download=str
        self.Print=str
        self.Action=str
        self.Created_by=str
        self.Created_on=str
        self.Modified_by=str
        self.Modified_on=str
@documents.Collection("sys.roles")
class Roles(object):
    def __init__(self):
        self.Code = str,True
        self.Name =str,True
        self.DDCode =str
        self.Description =str
        self.IsDelete = bool
        self.Privileges =RolePrivileges
        self.Created_by = str,True
        self.Created_on = str,True,datetime.datetime.now
        self.Modified_by = str
        self.Modified_on = str

