import pymqr
from pymqr import pydocs
from pymqr import documents
import datetime

@documents.Collection("sys.users")
class Users(object):
    class ChangePasswordInfo(documents.BaseEmbededDoc):
        def __init__(self):
            self.OldPassword=str
            self.Time=(datetime.datetime,datetime.datetime.now)
            self.TimeUtc=datetime.datetime
    class LoginInfo(documents.BaseEmbededDoc):
        def __init__(self):
            self.LoginTime=datetime.datetime
            self.SessionID=(str,'unknown')
            self.LoginTimeUTC = datetime.datetime
    class Profiles(documents.BaseEmbededDoc):
        def __init__(self):
            self.FirstName=str
            self.LastName=str
            self.Geder=(bool,True)
            self.BirthDate=datetime.datetime

    def __init__(self):
        self.Username=str
        self.PasswordSalt=str
        self.HashPassword=str
        self.Email=str
        self.PasswordChangeList=list
        self.Logins=(list,[])
        self.Profile=(Users.Profiles,{
             pydocs.document.LastName:"",
             pydocs.document.FirstName:"",
             pydocs.document.BirthDate:datetime.datetime.now

        })


# model = pymqr.create_model(
# users=Users()
# users.set_model_name("users")

