import pymqr
from pymqr import pydoc
from pymqr import documents
import datetime

class Users(documents.BaseDocuments):
    class ChangePasswordInfo(documents.BaseEmbededDoc):
        def __init__(self):
            self.OldPassword=str
            self.Time=datetime.datetime
            self.TimeUtc=datetime.datetime
    class LoginInfo(documents.BaseEmbededDoc):
        def __init__(self):
            self.LoginTime=datetime.datetime
            self.SessionID=str
            self.LoginTimeUTC = datetime.datetime
    class Profiles(documents.BaseEmbededDoc):
        def __init__(self):
            self.FirstName=str
            self.LastName=str
            self.Geder=bool
            self.BirthDate=datetime.datetime

    def __init__(self):
        self.Username=str
        self.PasswordSalt=str
        self.HashPassword=str
        self.Emai=str
        self.PasswordChangeList=list
        self.Logins=list
        self.Profile=Users.Profiles


# model = pymqr.create_model(
users=Users()
users.set_model_name("users")