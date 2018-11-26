import pymqr
import datetime
@pymqr.documents.EmbededDocument()
class UserInfo(object):
    def __init__(self):
        self.LoginAccount = str
        self.UserName =str
        self.DisplayName = str
        self.RoleCode =str
        self.Email = str
        self.IsSystem =bool
        self.ManLevelFrom = int
        self.MainLevelTo  = int
        self.Mobile =str
        self.Description =str
        self.CreatedOn=datetime.datetime
        self.CreatedBy = str
        self.ModifiedOn= datetime.datetime
        self.ModifiedBy =str


@pymqr.documents.Collection("users")
class Users(object):
    def __init__(self):
        self.Usernme=str
        self.FirstName =str
        self.LastName =str
        self.IsActive = bool
        self.Email =str
        self.IsSupperUser=bool
        self.IsStaff=bool
        self.LastLogin = datetime.datetime
        self.Password = str
        self.JointDate = datetime.datetime
        self.AccountInfo = UserInfo()


